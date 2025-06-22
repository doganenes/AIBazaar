import os
import io
import base64
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from django.conf import settings
from sklearn.model_selection import train_test_split
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from trainers.train_lstm_models import LSTMModelTrainer
from tensorflow.keras.models import load_model
import traceback

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold, cross_val_score
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pandas as pd


lstm_trainer = LSTMModelTrainer(
   data_path=r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\notebooks\LSTMPriceHistory.csv",
   model_dir=r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\models"
)


def find_similar_phones(df, predicted_price, user_os, user_specs, top_n=5):

    price_tolerance = 0.20
    min_price = predicted_price * (1 - price_tolerance)
    max_price = predicted_price * (1 + price_tolerance)

    user_os_clean = user_os.strip().title()
    if "Android" in user_os_clean:
        os_filter = df["os_type"].str.contains("Android", case=False, na=False)
    elif "Ios" in user_os_clean or "iOS" in user_os_clean:
        os_filter = df["os_type"].str.contains("Ios", case=False, na=False)
    else:
        os_filter = pd.Series([True] * len(df))  

  
    similar_phones = df[
        (df["price"] >= min_price) & (df["price"] <= max_price) & os_filter
    ].copy()

    if len(similar_phones) == 0:
      
        similar_phones = df[os_filter].copy()
        if len(similar_phones) == 0:
            return []

   
    def calculate_similarity_score(row):
        score = 0

    
        ram_diff = abs(row["ram"] - user_specs["ram"]) / user_specs["ram"]
        if ram_diff <= 0.5:
            score += 20
        elif ram_diff <= 1.0:
            score += 10

     
        storage_diff = (
            abs(row["storage"] - user_specs["storage"]) / user_specs["storage"]
        )
        if storage_diff <= 0.5:
            score += 15
        elif storage_diff <= 1.0:
            score += 8

        display_diff = (
            abs(row["display_size"] - user_specs["display_size"])
            / user_specs["display_size"]
        )
        if display_diff <= 0.1:
            score += 15
        elif display_diff <= 0.2:
            score += 10

      
        battery_diff = (
            abs(row["battery"] - user_specs["battery"]) / user_specs["battery"]
        )
        if battery_diff <= 0.2:
            score += 15
        elif battery_diff <= 0.4:
            score += 8

        
        camera_diff = abs(row["camera"] - user_specs["camera"]) / user_specs["camera"]
        if camera_diff <= 0.3:
            score += 10
        elif camera_diff <= 0.6:
            score += 5

      
        chipset_diff = abs(row["chipset"] - user_specs["chipset"])
        if chipset_diff <= 1:
            score += 10
        elif chipset_diff <= 2:
            score += 5

       
        if row["5g"] == user_specs["5g"]:
            score += 8

    
        refresh_diff = abs(row["refresh_rate"] - user_specs["refresh_rate"])
        if refresh_diff <= 30:
            score += 5

     
        price_diff = abs(row["price"] - predicted_price) / predicted_price
        if price_diff <= 0.1:
            score += 15
        elif price_diff <= 0.2:
            score += 10

        return score

    
    similar_phones["similarity_score"] = similar_phones.apply(
        calculate_similarity_score, axis=1
    )


    recommended_phones = similar_phones.nlargest(top_n, "similarity_score")

 
    recommendations = []
    for _, phone in recommended_phones.iterrows():
        recommendations.append(
            {
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
                "price_difference": round(
                    ((phone["price"] - predicted_price) / predicted_price) * 100, 1
                ),
                "product_id": phone.get("ProductID"),
            }
        )

    return recommendations


def feature_engineering(df):
  
    df["ram_storage"] = df["ram"] * df["storage"]
    df["battery_display_ratio"] = df["battery"] / df["display_size"]
    df["ppi_refresh"] = df["ppi_density"] * df["refresh_rate"]
    df["chipset_5g"] = df["chipset"] * df["5g"]

    df["is_android"] = (
        df["os_type"].str.contains("Android", case=False, na=False)
    ).astype(int)
    df["is_ios"] = (df["os_type"].str.contains("Ios", case=False, na=False)).astype(int)
    df["is_oled"] = (
        df["display_type"].str.contains("Oled", case=False, na=False)
    ).astype(int)

    df["log_battery"] = np.log1p(df["battery"])

   
    if "waterproof" in df.columns and "dustproof" in df.columns:
        df["protection_score"] = df["waterproof"] + df["dustproof"] 
        df["full_protection"] = (
            (df["waterproof"] == 1) & (df["dustproof"] == 1)
        ).astype(int)

    return df


@api_view(["POST"])
def predict_product_rf(request):
    try:
        data = request.data

        ram = float(data.get("RAM"))
        storage = float(data.get("Storage"))
        display_size = float(data.get("Display Size"))
        battery = float(data.get("Battery Capacity"))
        ppi = int(data.get("Pixel Density"))
        os = data.get("Operating System").strip().title()
        display_type = data.get("Display Technology").strip().split(",")[0].title()
        camera = float(data.get("camera"))
        chipset = int(data.get("CPU Manufacturing"))
        is_5g = 1 if data.get("5G") == "Yes" else 0
        refresh_rate = int(data.get("Refresh Rate", 60))
        waterproof = int(data.get("Waterproof", 0))  
        dustproof = int(data.get("Dustproof", 0)) 

        df = pd.read_csv(
            r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\notebooks\product_specs_en.csv"
        )

     
        df.rename(
            columns={
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
            },
            inplace=True,
        )

        df["os_type"] = df["os_type"].str.strip().str.title()
        df["display_type"] = (
            df["display_type"].str.strip().str.split(",").str[0].str.title()
        )

      
        if "waterproof" not in df.columns:
            df["waterproof"] = 0  # Varsayılan olarak waterproof değil
        if "dustproof" not in df.columns:
            df["dustproof"] = 0  

       
        numeric_columns = [
            "ram",
            "storage",
            "display_size",
            "battery",
            "ppi_density",
            "camera",
            "chipset",
            "5g",
            "refresh_rate",
            "waterproof",
            "dustproof",
            "price",
        ]

        for col in numeric_columns:
            if col in df.columns:
               
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # df = df.dropna(subset=numeric_columns)

        if len(df) < 10:
            return Response(
                {"error": "Insufficient clean data for training"}, status=400
            )

       
        df = feature_engineering(df)

        feature_columns = [
            "ram",
            "storage",
            "display_size",
            "battery",
            "ppi_density",
            "os_type",
            "display_type",
            "camera",
            "chipset",
            "5g",
            "refresh_rate",
            "waterproof", 
            "dustproof",        
            "ram_storage",
            "battery_display_ratio",
            "ppi_refresh",
            "chipset_5g",
            "is_android",
            "is_ios",
            "is_oled",
            "log_battery",
            "protection_score",
            "full_protection",
        ]

        X = df[feature_columns].copy()
        y = df["price"]

        le_os = LabelEncoder()
        X["os_type"] = le_os.fit_transform(X["os_type"])

        le_display = LabelEncoder()
        X["display_type"] = le_display.fit_transform(X["display_type"])

        new_data = pd.DataFrame(
            [
                {
                    "ram": ram,
                    "storage": storage,
                    "display_size": display_size,
                    "battery": battery,
                    "ppi_density": ppi,
                    "os_type": os,
                    "display_type": display_type,
                    "camera": camera,
                    "chipset": chipset,
                    "5g": is_5g,
                    "refresh_rate": refresh_rate,
                    "waterproof": waterproof, 
                    "dustproof": dustproof,
                }
            ]
        )

       
        new_data = feature_engineering(new_data)

      
        try:
            new_data["os_type"] = le_os.transform(new_data["os_type"])
        except ValueError:
           
            most_common_os = df["os_type"].mode()[0]
            new_data["os_type"] = le_os.transform([most_common_os])

        try:
            new_data["display_type"] = le_display.transform(new_data["display_type"])
        except ValueError:
           
            most_common_display = df["display_type"].mode()[0]
            new_data["display_type"] = le_display.transform([most_common_display])

     
        model = RandomForestRegressor(
            n_estimators=200,
            max_depth=15,
            random_state=42,
            n_jobs=-1,
        )

 
        cv = KFold(n_splits=5, shuffle=True, random_state=42)
        scores = cross_val_score(model, X, y, scoring="r2", cv=cv, n_jobs=-1)

        mean_r2 = round(np.mean(scores), 4)
        std_r2 = round(np.std(scores), 4)
   
        model.fit(X, y)

        prediction = model.predict(new_data)[0]
        user_specs = {
            "ram": ram,
            "storage": storage,
            "display_size": display_size,
            "battery": battery,
            "camera": camera,
            "chipset": chipset,
            "5g": is_5g,
            "refresh_rate": refresh_rate
        }
        similar_phones = find_similar_phones(df, prediction, os, user_specs, top_n=1)
        print("Similar Phones:", similar_phones)
        return Response(
            {
                "message": "Random Forest prediction successful",
                "price": round(prediction, 2),
                "cv_scores": {
                    "r2_mean": mean_r2,
                    "r2_std": std_r2,
                },
                "features_used": {
                    "waterproof": waterproof,
                    "dustproof": dustproof,
                    "protection_score": waterproof + dustproof,
                    "full_protection": 1 if (waterproof == 1 and dustproof == 1) else 0,
                },
                "recommendations": {
                    "similar_phones": similar_phones,
                    "recommendation_count": len(similar_phones),
                    "recommendation_criteria": {
                        "price_range": f"±20% ({round(prediction * 0.8, 2)} - {round(prediction * 1.2, 2)})",
                        "os_restriction": f"Only {os} phones",
                        "flexibility": "RAM/Storage can be ±50%, other specs ±20-40%",
                    }
                },
            }
        )

    except Exception as e:
        traceback.print_exc()
        return Response({"error": str(e)}, status=400)



@api_view(["POST"])
def predict_product_lstm(request):
    try:
        product_id = request.data.get("productId")
        if product_id is None:
            return Response({"error": "productId is required."}, status=status.HTTP_400_BAD_REQUEST)

        df = lstm_trainer.load_data()
        product_df = df[df["ProductID"] == int(product_id)]

        if product_df.empty:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        result = lstm_trainer.predict_price(product_id=product_id, steps=15)

        return Response(result, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
