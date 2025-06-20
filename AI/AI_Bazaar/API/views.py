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

lstm_trainer = LSTMModelTrainer(
    data_path=r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\notebooks\LSTMPriceHistory.csv",
    model_dir=r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\models"
)


@api_view(["POST"])
def predict_product_xgboost(request):
    data = request.data

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
            r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\notebooks\Product.csv"
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
            "Refresh Rate": "refresh_rate"
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
            "refresh_rate"
        ]
        df = df[features + ["price", "phone_model"]]

        os_hierarchy = {
            "Android": 1,
            "iOS": 2,
        }

        display_type_hierarchy = {
            "PLS LCD": 1,
            "IPS LCD": 2,
            "OLED": 3,
            "AMOLED": 4,
            "Super AMOLED": 5,
            "Dynamic AMOLED": 6,
            "Super Retina XDR OLED": 7,
            "LTPO Super Retina XDR OLED": 8,
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

        # Initialize and train XGBoost model
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
        closest_product = df.loc[df["price_diff"].idxmin()]

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
                "closest_product": closest_product["phone_model"],
            }
        )

    except Exception as e:
        print(f"Error in XGBoost prediction: {str(e)}")
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
