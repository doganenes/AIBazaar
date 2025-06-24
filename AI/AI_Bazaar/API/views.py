import os
import io
import base64
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from django.conf import settings
from sklearn.model_selection import train_test_split, GridSearchCV
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import traceback
from scipy import stats
import warnings
import joblib 
import pickle 
from datetime import datetime

warnings.filterwarnings('ignore')
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
import pandas as pd
import traceback

RF_MODEL_PATH = r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\models\phone_price_model_20250624_182007.pkl"

RF_DATA_PATH = r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\notebooks\Product.csv"

def advanced_feature_engineering(df):
    
    df["ram_storage"] = df["ram"] * df["storage"]
    df["battery_display_ratio"] = df["battery"] / (df["display_size"] + 0.1) 
    df["ppi_refresh"] = df["ppi_density"] * df["refresh_rate"]
    df["chipset_5g"] = df["chipset"] * (df["5g"] + 1)  
    
    df["performance_score"] = (df["ram"] * df["chipset"] * df["refresh_rate"]) / 1000
    df["premium_score"] = (df["camera"] * df["ppi_density"] * df["refresh_rate"]) / 10000
    df["storage_efficiency"] = df["storage"] / (df["ram"] + 1)
    df["display_quality"] = df["ppi_density"] * df["display_size"] * df["refresh_rate"] / 1000
    df["battery_efficiency"] = df["battery"] / df["display_size"]
    
    df["is_android"] = (df["os_type"].str.contains("Android", case=False, na=False)).astype(int)
    df["is_ios"] = (df["os_type"].str.contains("Ios", case=False, na=False)).astype(int)
    df["is_oled"] = (df["display_type"].str.contains("Oled", case=False, na=False)).astype(int)
    df["is_amoled"] = (df["display_type"].str.contains("Amoled", case=False, na=False)).astype(int)
    

    df["log_battery"] = np.log1p(df["battery"])
    df["log_ram"] = np.log1p(df["ram"])
    df["log_storage"] = np.log1p(df["storage"])
    df["log_camera"] = np.log1p(df["camera"])
    
    df["flagship_indicator"] = ((df["ram"] >= 8) & (df["storage"] >= 128) & 
                              (df["camera"] >= 48) & (df["5g"] == 1)).astype(int)
    df["budget_indicator"] = ((df["ram"] <= 4) & (df["storage"] <= 64)).astype(int)
    df["mid_range_indicator"] = ((df["ram"].between(4, 8)) & 
                                (df["storage"].between(64, 256))).astype(int)
    
    df["tech_generation"] = np.where(df["chipset"] <= 14, 0, 
                                   np.where(df["chipset"] <= 7, 1,   
                                          np.where(df["chipset"] <= 5, 2, 3))) 
    

    if "waterproof" in df.columns and "dustproof" in df.columns:
        df["protection_score"] = df["waterproof"] + df["dustproof"]
        df["full_protection"] = ((df["waterproof"] == 1) & (df["dustproof"] == 1)).astype(int)
    else:
        df["protection_score"] = 0
        df["full_protection"] = 0
    
    if "price" in df.columns:
        df["price_segment"] = pd.qcut(df["price"], q=4, labels=['Budget', 'Mid', 'Premium', 'Flagship'])
    
    return df


def load_model_package(model_path):
    try:
        if model_path.endswith('.pkl') and 'pickle' not in model_path:
            model_package = joblib.load(model_path)
        else:
            with open(model_path, 'rb') as f:
                model_package = pickle.load(f)
        
        return model_package
    except Exception as e:
        print(f"Model yükleme hatası: {e}")
        return None


def remove_outliers(df, columns, method='iqr'):
    df_clean = df.copy()
    
    for col in columns:
        if col in df_clean.columns:
            if method == 'iqr':
                Q1 = df_clean[col].quantile(0.25)
                Q3 = df_clean[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                df_clean = df_clean[(df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)]
            elif method == 'zscore':
                z_scores = np.abs(stats.zscore(df_clean[col]))
                df_clean = df_clean[z_scores < 3]
    
    return df_clean

def find_similar_phones(df, predicted_price, user_os, user_specs, top_n=5):
    
    price_tolerance = 0.25 
    min_price = predicted_price * (1 - price_tolerance)
    max_price = predicted_price * (1 + price_tolerance)
    
    user_os_clean = user_os.strip().title()
    if "Android" in user_os_clean:
        os_filter = df["os_type"].str.contains("Android", case=False, na=False)
    elif "Ios" in user_os_clean or "iOS" in user_os_clean:
        os_filter = df["os_type"].str.contains("Ios", case=False, na=False)
    else:
        os_filter = pd.Series([True] * len(df))
    
    similar_phones = df[(df["price"] >= min_price) & (df["price"] <= max_price) & os_filter].copy()
    
    if len(similar_phones) == 0:
        similar_phones = df[os_filter].copy()
        if len(similar_phones) == 0:
            return []
    
    def calculate_similarity_score(row):
        score = 0
        
        weights = {
            'ram': 25,
            'storage': 20,
            'display_size': 15,
            'battery': 15,
            'camera': 12,
            'chipset': 10,
            '5g': 8,
            'refresh_rate': 5,
            'price': 20
        }
        
        for spec, weight in weights.items():
            if spec in user_specs and spec in row.index:
                if user_specs[spec] != 0: 
                    diff = abs(row[spec] - user_specs[spec]) / user_specs[spec]
                    if diff <= 0.2:
                        score += weight
                    elif diff <= 0.5:
                        score += weight * 0.7
                    elif diff <= 1.0:
                        score += weight * 0.3
        
        if predicted_price != 0:
            price_diff = abs(row["price"] - predicted_price) / predicted_price
            if price_diff <= 0.1:
                score += 25
            elif price_diff <= 0.2:
                score += 15
            elif price_diff <= 0.3:
                score += 8
        
        return score
    
    similar_phones["similarity_score"] = similar_phones.apply(calculate_similarity_score, axis=1)
    recommended_phones = similar_phones.nlargest(top_n, "similarity_score")
    
    recommendations = []
    for _, phone in recommended_phones.iterrows():
        recommendations.append({
            "model": phone.get("phone_model", "Unknown Model"),
            "price": round(phone["price"], 2),
            "ram": int(phone["ram"]),
            "storage": int(phone["storage"]),
            "display_size": phone["display_size"],
            "battery": int(phone["battery"]),
            "camera": phone["camera"],
            "os": phone["os_type"],
            "display_type": phone["display_type"],
            "chipset": int(phone["chipset"]),
            "5g": int(phone["5g"]),
            "refresh_rate": int(phone["refresh_rate"]),
            "similarity_score": round(phone["similarity_score"], 2),
            "price_difference": round(((phone["price"] - predicted_price) / predicted_price) * 100, 1),
            "product_id": phone.get("ProductID", "N/A"),
        })
    
    return recommendations

@api_view(["POST"])
def predict_product_rf(request, model_path=RF_MODEL_PATH):
    try:
        model_path = request.data.get("model_path", model_path)
        if not model_path or not os.path.exists(model_path):
            return Response({"error": "Model dosyası bulunamadı"}, status=400)

        model_package = load_model_package(model_path)
        if not model_package:
            return Response({"error": "Model yüklenemedi"}, status=400)

        model = model_package['model']
        le_os = model_package['label_encoder_os']
        le_display = model_package['label_encoder_display']
        feature_columns = model_package['feature_columns']
        model_info = model_package['model_info']

        data = request.data
        ram = float(data.get("RAM"))
        storage = float(data.get("Storage"))
        display_size = float(data.get("Display Size"))
        battery = float(data.get("Battery Capacity"))
        ppi = int(data.get("Pixel Density"))
        os_name = data.get("Operating System").strip().title()
        display_type = data.get("Display Technology").strip().split(",")[0].title()
        camera = float(data.get("camera"))
        chipset = int(data.get("CPU Manufacturing"))
        is_5g = 1 if data.get("5G") == "Yes" else 0
        refresh_rate = int(data.get("Refresh Rate", 60))
        waterproof = int(data.get("Waterproof", 0))
        dustproof = int(data.get("Dustproof", 0))

        new_data = pd.DataFrame([{
            "ram": ram, "storage": storage, "display_size": display_size,
            "battery": battery, "ppi_density": ppi, "os_type": os_name,
            "display_type": display_type, "camera": camera, "chipset": chipset,
            "5g": is_5g, "refresh_rate": refresh_rate, "waterproof": waterproof, 
            "dustproof": dustproof
        }])

        new_data = advanced_feature_engineering(new_data)

        # Encoding
        try:
            new_data["os_encoded"] = le_os.transform(new_data["os_type"])
        except ValueError:
            return Response({"error": f"Bilinmeyen OS türü: {os_name}"}, status=400)

        try:
            new_data["display_encoded"] = le_display.transform(new_data["display_type"])
        except ValueError:
            return Response({"error": f"Bilinmeyen display türü: {display_type}"}, status=400)

        prediction = model.predict(new_data[feature_columns])[0]

        df = pd.read_csv(RF_DATA_PATH)
        
        df.rename(columns={
            "RAM": "ram",
            "Internal Storage": "storage",
            "Display Size": "display_size",
            "Battery Capacity": "battery",
            "Pixel Density": "ppi_density",
            "Operating System": "os_type",
            "Display Technology": "display_type",
            "Camera Resolution": "camera",
            "CPU Manufacturing": "chipset",
            "Price": "price",
            "5G": "5g",
            "Model": "phone_model",
            "Refresh Rate": "refresh_rate",
            "Waterproof": "waterproof",
            "Dustproof": "dustproof",
        }, inplace=True)

        df["os_type"] = df["os_type"].str.strip().str.title()
        df["display_type"] = df["display_type"].str.strip().str.split(",").str[0].str.title()

        if "waterproof" not in df.columns:
            df["waterproof"] = 0
        if "dustproof" not in df.columns:
            df["dustproof"] = 0

        numeric_columns = ["ram", "storage", "display_size", "battery", "ppi_density", 
                          "camera", "chipset", "5g", "refresh_rate", "waterproof", "dustproof", "price"]

        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        df_clean = df.dropna(subset=numeric_columns)

        df_clean = advanced_feature_engineering(df_clean)

        user_specs = {
            "ram": ram, "storage": storage, "display_size": display_size,
            "battery": battery, "camera": camera, "chipset": chipset,
            "5g": is_5g, "refresh_rate": refresh_rate
        }
        
        similar_phones = find_similar_phones(df_clean, prediction, os_name, user_specs, top_n=3)

        return Response({
            "message": "Kaydedilmiş model ile tahmin başarılı",
            "price": round(prediction, 2),
            "model_info": model_info,
            "model_version": model_package.get('version', 'Unknown'),
            "model_timestamp": model_package.get('timestamp', 'Unknown'),
            "recommendations": {
                "similar_phones": similar_phones,
                "recommendation_count": len(similar_phones),
                "recommendation_criteria": {
                    "price_range": f"±25% ({round(prediction * 0.75, 2)} - {round(prediction * 1.25, 2)})",
                    "os_restriction": f"Only {os_name} phones",
                    "flexibility": "Weighted similarity scoring with advanced features"
                }
            }
        })

    except Exception as e:
        traceback.print_exc()
        return Response({"error": str(e)}, status=400)