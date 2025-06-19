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


@api_view(["POST"])
def predict_product_xgboost(request):
    data = request.data

    try:
        ram = float(data.get("ram"))
        storage = float(data.get("storage"))
        display_size = float(data.get("display_size"))
        battery = float(data.get("battery"))
        quick_charge = int(data.get("quick_charge"))
        ppi = int(data.get("ppi"))
        os = data.get("os_type")
        display_type = data.get("display_type")
        camera = float(data.get("camera"))
        chipset = int(data.get("chipset"))

        df = pd.read_csv(
            r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\filterPhone.csv"
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
        ]
        df = df[features + ["price", "phone_model"]]

        os_hierarchy = {
            "HarmonyOS": 1,
            "EMUI": 2,
            "Android": 3,
            "iOS": 4,
        }

        display_type_hierarchy = {
            "PLS LCD": 1,
            "IPS LCD": 2,
            "OLED": 3,
            "AMOLED": 4,
            "Super AMOLED": 5,
            "Dynamic LTPO AMOLED 2X": 6,
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

        df["chipset"] = df["chipset"].apply(
            lambda x: (
                int("".join(filter(str.isdigit, x.split("(")[-1].split("nm")[0])))
                if isinstance(x, str) and "(" in x and "nm" in x
                else 0
            )
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
                }
            ]
        )

        scaler = StandardScaler()
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model = xgb.XGBRegressor(
            objective="reg:squarederror",
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_alpha=0.1,
            reg_lambda=0.1,
        )

        model.fit(X_train, y_train)

        prediction_price = model.predict(new_data)[0]

        print(f"Predicted price: {round(prediction_price, 2)}")
        print(
            f"Input encodings - OS: {os_encoded}, Display: {display_type_encoded}"
        )

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


trainer = LSTMModelTrainer(
    data_path=r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\notebooks\LSTMPriceHistory.csv",
    model_dir=r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\models"
)

from tensorflow.keras.models import load_model

@api_view(["POST"])
def predict_product_lstm(request):
    try:
        product_name = request.data.get("product")
        steps = int(request.data.get("steps", 15))

        if not product_name:
            return Response({"error": "Product name is required."}, status=400)

        result = trainer.predict_price(product_name, steps)
        return Response(result)

    except Exception as e:
        return Response({"error": str(e)}, status=400)
