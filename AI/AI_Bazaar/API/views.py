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
import xgboost as xgb
from tensorflow.keras.models import load_model

# lstm_trainer = LSTMModelTrainer(
#    data_path=r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\notebooks\LSTMPriceHistory.csv",
#    model_dir=r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\models"
# )


@api_view(["POST"])
def predict_product_xgboost(request):
    data = request.data
    print("Received data:", data)

    try:
        ram = float(data.get("RAM"))
        storage = float(data.get("Storage"))
        display_size = float(data.get("Display Size"))
        battery = float(data.get("Battery Capacity"))
        quick_charge = int(data.get("Quick Charge"))
        ppi = int(data.get("Pixel Density"))
        os = data.get("Operating System")
        display_type = data.get("Display Technology")
        camera = float(data.get("camera"))
        chipset = int(data.get("CPU Manufacturing"))

        df = pd.read_csv(
            r"C:\Users\pc\Desktop\AIbazaar\AIBazaar\AI\utils\notebooks\Product.csv"
        )

        df.rename(
        columns={
            "RAM": "ram",
            "Internal Storage": "storage",
            "Display Size": "display_size",
            "Battery Capacity": "battery",
            "Fast Charging": "quick_charge",
            "Pixel Density": "ppi_density",
            "Operating System": "os_type",
            "Display Technology": "display_type",
            "Camera Resolution": "camera",
            "CPU Manufacturing": "chipset",
            "Price": "price",
            "5G" : "5g",
            "Model": "phone_model",
            "Refresh Rate": "refresh_rate",
        },
        inplace=True
    )

        features = [
            "ram",
            "storage",
            "display_size",
            "battery",
            "quick_charge",
            "ppi_density",
            "os_type",
            "display_type",
            "camera",
            "chipset",
            "5g",
            "refresh_rate",
        ]

        df = df[features + ["price", "phone_model","ProductID"]]

        os_hierarchy = {
            "Android": 1,
            "iOS": 2,
        }

        display_type_hierarchy = {
            "IPS LCD": 1.00,
            "PLS LCD": 1.09,
            "OLED": 8.02,
            "AMOLED": 2.92,
            "Super AMOLED": 2.28,
            "Dynamic AMOLED": 6.04,
            "Other": 0,
        }

        def safe_map(value, mapping, default=0):
            return mapping.get(value, default)

        df["os_encoded"] = df["os_type"].apply(lambda x: safe_map(x, os_hierarchy))
        df["display_type"] = df["display_type"].apply(lambda x: x.split(",")[0].strip())
        df["display_type_encoded"] = df["display_type"].apply(
            lambda x: safe_map(x, display_type_hierarchy)
        )

        os_encoded = safe_map(os, os_hierarchy)
        display_type_encoded = safe_map(display_type, display_type_hierarchy)

        feature_columns = [
            "ram",
            "storage",
            "display_size",
            "battery",
            "quick_charge",
            "ppi_density",
            "os_encoded",
            "display_type_encoded",
            "camera",
            "chipset",
            "5g",
            "refresh_rate"
        ]

        X = df[feature_columns]
        y = df["price"]

        new_data = pd.DataFrame(
            [
                {
                    "ram": ram,
                    "storage": storage,
                    "display_size": display_size,
                    "battery": battery,
                    "quick_charge": quick_charge,
                    "ppi_density": ppi,
                    "os_encoded": os_encoded,
                    "display_type_encoded": display_type_encoded,
                    "camera": camera,
                    "chipset": chipset,
                    "5g": 1 if data.get("5G") == "Yes" else 0,
                    "refresh_rate": int(data.get("Refresh Rate", 60)),
                }
            ]
        )

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )

        model = xgb.XGBRegressor(
            objective="reg:squarederror",
            n_estimators=150,          
            max_depth=8,                
            learning_rate=0.05,         
            random_state=42,
            subsample=0.7,              
            colsample_bytree=0.7,       
            reg_alpha=0.05,              
            reg_lambda=0.05,            
            min_child_weight=1,         
            gamma=0,                   
            importance_type='gain'     
    )

        model.fit(X_train, y_train)

        prediction_price = model.predict(scaler.transform(new_data))[0]

        feature_importance = dict(zip(feature_columns, model.feature_importances_))
        top_features = sorted(
            feature_importance.items(), key=lambda x: x[1], reverse=True
        )[:10]

        df["price_diff"] = (df["price"] - prediction_price).abs()
        df = df[(df["price_diff"] <= prediction_price * 1.15) & (df["price_diff"] >= prediction_price * 0.85)]

        df["os_type"] = df["os_type"].str.strip().str.lower()
        os = os.strip().lower()

        df["display_type"] = df["display_type"].str.strip().str.lower()
        display_type = display_type.strip().lower()
        print("Filtered DataFrame after price difference:", df.head(5))
        df.to_csv("filtered_products.csv", index=False)
        tolerance = 0.9
        print("collums ",df.columns)
        tolerance = 25  # %20 aralık

        filtered_df = df[
            (df["ram"].between(ram * (1 - tolerance), ram * (1 + tolerance))) &
            (df["storage"].between(storage * (1 - tolerance), storage * (1 + tolerance))) &
            (df["display_size"].between(display_size * (1 - tolerance), display_size * (1 + tolerance))) &
            (df["battery"].between(battery * (1 - tolerance), battery * (1 + tolerance))) &
            (df["quick_charge"] == quick_charge) &
            (df["ppi_density"].between(ppi * (1 - tolerance), ppi * (1 + tolerance))) &
            (df["camera"].between(camera * (1 - tolerance), camera * (1 + tolerance))) &
            (df["chipset"].between(chipset * (1 - tolerance), chipset * (1 + tolerance))) &
            (df["os_type"] == os) &
            (df["display_type"] == display_type)
        ]
        
        # Eğer filtreleme sonucu telefon bulunamazsa, toleransı artır
        if filtered_df.empty:
            print(f"Tolerance %{tolerance*100} ile telefon bulunamadı, tolerance artırılıyor...")
            for new_tolerance in [0.3, 0.4, 0.5]:
                filtered_df = df[
                    (df["ram"].between(ram * (1 - new_tolerance), ram * (1 + new_tolerance))) &
                    (df["storage"].between(storage * (1 - new_tolerance), storage * (1 + new_tolerance))) &
                    (df["display_size"].between(display_size * (1 - new_tolerance), display_size * (1 + new_tolerance))) &
                    (df["battery"].between(battery * (1 - new_tolerance), battery * (1 + new_tolerance))) &
                    (df["ppi_density"].between(ppi * (1 - new_tolerance), ppi * (1 + new_tolerance))) &
                    (df["camera"].between(camera * (1 - new_tolerance), camera * (1 + new_tolerance))) &
                    (df["chipset"].between(chipset * (1 - new_tolerance), chipset * (1 + new_tolerance)))
                ]
                
                # Kategorik özellikler için ayrı filtreleme
                if not filtered_df.empty:
                    # Önce kategorik özellikleri de kontrol et
                    exact_match = filtered_df[
                        (filtered_df["quick_charge"] == quick_charge) &
                        (filtered_df["os_type"] == os) &
                        (filtered_df["display_type"] == display_type)
                    ]
                    
                    if not exact_match.empty:
                        filtered_df = exact_match
                        break
                    else:
                        # Kategorik özelliklerden taviz ver
                        print(f"Kategorik özellikler tam eşleşmiyor, tolerance %{new_tolerance*100} ile devam ediliyor...")
                        break
        
        # Hala telefon bulunamazsa, sadece en önemli özelliklere odaklan
        if filtered_df.empty:
            print("Hiçbir telefon bulunamadı, sadece temel özelliklere göre arama yapılıyor...")
            filtered_df = df[
                (df["ram"].between(ram * 0.7, ram * 1.3)) &
                (df["storage"].between(storage * 0.7, storage * 1.3)) &
                (df["battery"].between(battery * 0.7, battery * 1.3))
            ]
        
        if filtered_df.empty:
            return None, "Hiçbir uygun telefon bulunamadı!"
        
        # Filtrelenmiş telefonlar arasından en yakınını bul
        user_values = np.array([ram, storage, display_size, battery, ppi, camera, chipset])
        
        distances = []
        for idx, phone in filtered_df.iterrows():
            phone_values = np.array([
                phone['ram'], phone['storage'], phone['display_size'], 
                phone['battery'], phone['ppi_density'], phone['camera'], phone['chipset']
            ])
            
            # Normalize edilmiş mesafe hesapla
            normalized_diff = abs(phone_values - user_values) / user_values
            distance = np.mean(normalized_diff)  # Ortalama yüzde fark
            distances.append(distance)
        
        # En küçük mesafeye sahip telefonu seç
        best_index = np.argmin(distances)
        best_phone = filtered_df.iloc[best_index]
        best_distance = distances[best_index]



        print("Filtered DataFrame:", df)
        if df.empty:
            return Response({"error": "No similar product found after filtering."}, status=status.HTTP_404_NOT_FOUND)

        # Tüm benzer ürünleri döndür
        similar_products = df.sort_values(by="price").to_dict(orient="records")
        print("Similar products found:", similar_products)
        return Response(
            {
                "message": "XGBoost prediction successful",
                "price": round(prediction_price, 2),
                "encodings": {
                    "os": os_encoded,
                    "display_type": display_type_encoded,
                },
                "model_info": {
                    "algorithm": "XGBoost",
                    "top_features": [
                        {"feature": feat, "importance": round(imp, 4)}
                        for feat, imp in top_features
                    ],
                },
                "similar_products": similar_products
            }
        )

    except Exception as e:
        print(f"Error in XGBoost prediction: {str(e)}")
        return Response({"error": str(e)}, status=400)

'''    
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
'''
