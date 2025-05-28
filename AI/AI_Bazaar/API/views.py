import base64
import io
from matplotlib import pyplot as plt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from sklearn.neighbors import KNeighborsRegressor
import pandas as pd
import os
from django.conf import settings
from statsmodels.tsa.arima.model import ARIMA
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import xgboost as xgb

import pandas as pd
import xgboost as xgb
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sklearn.preprocessing import StandardScaler

@api_view(["POST"])
def predict_product_xgboost(request):
    data = request.data

    try:
        # Input verilerini al
        ram = float(data.get("ram"))
        storage = float(data.get("storage"))
        display_size = float(data.get("display_size"))
        battery = float(data.get("battery"))
        foldable = int(data.get("foldable"))
        ppi = int(data.get("ppi"))
        os = data.get("os")
        display_type = data.get("display_type")
        video_resolution = data.get("video_resolution")
        chipset = int(data.get("chipset"))
        
        # CSV dosyasını oku
        df = pd.read_csv(
            r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\csv\phones.csv"
        )

        # Gerekli özellikleri seç
        features = [
            "ram",
            "storage",
            "display_size",
            "battery",
            "foldable",
            "ppi_density",
            "os",
            "display_type",
            "video_resolution",
            "chipset",
        ]
        df = df[features + ["price_usd"]]

        # Hiyerarşik encoding'ler
        os_hierarchy = {
            "Android": 1,
            "iOS": 2,
            "HarmonyOS": 1.5,  
            "Windows": 0.5,
            "Other": 0,
        }

        display_type_hierarchy = {
            "LCD": 1,
            "IPS LCD": 2,
            "OLED": 3,
            "AMOLED": 4,
            "Super AMOLED": 5,
            "Dynamic AMOLED": 6,
            "LTPO OLED": 7,
            "Other": 0,
        }

        video_resolution_hierarchy = {
            "480p": 1,
            "720p": 2,
            "HD": 2,
            "1080p": 3,
            "Full HD": 3,
            "1440p": 4,
            "QHD": 4,
            "2K": 4,
            "4K": 5,
            "UHD": 5,
            "8K": 6,
            "Other": 0,
        }

        def safe_map(value, mapping, default=0):
            """Güvenli mapping fonksiyonu - eğer değer mapping'de yoksa default değer döner"""
            return mapping.get(value, default)

        # Kategorik değişkenleri encode et
        df["os_encoded"] = df["os"].apply(lambda x: safe_map(x, os_hierarchy))
        df["display_type_encoded"] = df["display_type"].apply(
            lambda x: safe_map(x, display_type_hierarchy)
        )
        df["video_resolution_encoded"] = df["video_resolution"].apply(
            lambda x: safe_map(x, video_resolution_hierarchy)
        )

        # Chipset değerini işle
        df["chipset"] = df["chipset"].apply(
            lambda x: int(
                ''.join(filter(str.isdigit, x.split("(")[-1].split("nm")[0]))
            ) if isinstance(x, str) and "(" in x and "nm" in x else 0
        )

        # Input verilerini encode et
        os_encoded = safe_map(os, os_hierarchy)
        display_type_encoded = safe_map(display_type, display_type_hierarchy)
        video_resolution_encoded = safe_map(
            video_resolution, video_resolution_hierarchy
        )

        # Feature columns
        feature_columns = [
            "ram",
            "storage",
            "display_size",
            "battery",
            "foldable",
            "ppi_density",
            "os_encoded",
            "display_type_encoded",
            "video_resolution_encoded",
            "chipset",
        ]

        # Features ve target ayrımı
        X = df[feature_columns]
        y = df["price_usd"]

        # Yeni veri için DataFrame oluştur
        new_data = pd.DataFrame(
            [
                {
                    "ram": ram,
                    "storage": storage,
                    "display_size": display_size,
                    "battery": battery,
                    "foldable": foldable,
                    "ppi_density": ppi,
                    "os_encoded": os_encoded,
                    "display_type_encoded": display_type_encoded,
                    "video_resolution_encoded": video_resolution_encoded,
                    "chipset": chipset
                }
            ]
        )

        # Veri ölçeklendirme (XGBoost için opsiyonel ama performansı artırabilir)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        new_data_scaled = scaler.transform(new_data)

        # XGBoost modeli oluştur ve eğit
        model = xgb.XGBRegressor(
            objective="reg:squarederror",
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_alpha=0.1,
            reg_lambda=0.1
        )
        
        model.fit(X_scaled, y)

        # Tahmin yap
        prediction_price = model.predict(new_data_scaled)[0]

        print(f"Predicted price: {round(prediction_price, 2)}")
        print(
            f"Input encodings - OS: {os_encoded}, Display: {display_type_encoded}, Resolution: {video_resolution_encoded}"
        )

        # Feature importance bilgisi (opsiyonel)
        feature_importance = dict(zip(feature_columns, model.feature_importances_))
        top_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:3]

        return Response(
            {
                "message": "XGBoost prediction successful",
                "price": round(prediction_price, 2),
                "encodings": {
                    "os": os_encoded,
                    "display_type": display_type_encoded,
                    "video_resolution": video_resolution_encoded,
                },
                "model_info": {
                    "algorithm": "XGBoost",
                    "top_features": [{"feature": feat, "importance": round(imp, 4)} for feat, imp in top_features]
                }
            }
        )

    except Exception as e:
        print(f"Error in XGBoost prediction: {str(e)}")
        return Response({"error": str(e)}, status=400)


# Alternatif olarak, daha basit XGBoost versiyonu (ölçeklendirme olmadan)
@api_view(["POST"])
def predict_product_xgboost_simple(request):
    data = request.data

    try:
        # Input verilerini al
        ram = float(data.get("ram"))
        storage = float(data.get("storage"))
        display_size = float(data.get("display_size"))
        battery = float(data.get("battery"))
        foldable = int(data.get("foldable"))
        ppi = int(data.get("ppi"))
        os = data.get("os")
        display_type = data.get("display_type")
        video_resolution = data.get("video_resolution")
        chipset = int(data.get("chipset"))
        
        # CSV dosyasını oku
        df = pd.read_csv(
            r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\csv\phones.csv"
        )

        # Gerekli özellikleri seç
        features = [
            "ram",
            "storage",
            "display_size",
            "battery",
            "foldable",
            "ppi_density",
            "os",
            "display_type",
            "video_resolution",
            "chipset",
        ]
        df = df[features + ["price_usd"]]

        # Hiyerarşik encoding'ler
        os_hierarchy = {
            "Android": 1,
            "iOS": 2,
            "HarmonyOS": 1.5,  
            "Windows": 0.5,
            "Other": 0,
        }

        display_type_hierarchy = {
            "LCD": 1,
            "IPS LCD": 2,
            "OLED": 3,
            "AMOLED": 4,
            "Super AMOLED": 5,
            "Dynamic AMOLED": 6,
            "LTPO OLED": 7,
            "Other": 0,
        }

        video_resolution_hierarchy = {
            "480p": 1,
            "720p": 2,
            "HD": 2,
            "1080p": 3,
            "Full HD": 3,
            "1440p": 4,
            "QHD": 4,
            "2K": 4,
            "4K": 5,
            "UHD": 5,
            "8K": 6,
            "Other": 0,
        }

        def safe_map(value, mapping, default=0):
            """Güvenli mapping fonksiyonu"""
            return mapping.get(value, default)

        # Kategorik değişkenleri encode et
        df["os_encoded"] = df["os"].apply(lambda x: safe_map(x, os_hierarchy))
        df["display_type_encoded"] = df["display_type"].apply(
            lambda x: safe_map(x, display_type_hierarchy)
        )
        df["video_resolution_encoded"] = df["video_resolution"].apply(
            lambda x: safe_map(x, video_resolution_hierarchy)
        )

        # Chipset değerini işle
        df["chipset"] = df["chipset"].apply(
            lambda x: int(
                ''.join(filter(str.isdigit, x.split("(")[-1].split("nm")[0]))
            ) if isinstance(x, str) and "(" in x and "nm" in x else 0
        )

        # Input verilerini encode et
        os_encoded = safe_map(os, os_hierarchy)
        display_type_encoded = safe_map(display_type, display_type_hierarchy)
        video_resolution_encoded = safe_map(
            video_resolution, video_resolution_hierarchy
        )

        # Feature columns
        feature_columns = [
            "ram",
            "storage",
            "display_size",
            "battery",
            "foldable",
            "ppi_density",
            "os_encoded",
            "display_type_encoded",
            "video_resolution_encoded",
            "chipset",
        ]

        # Features ve target ayrımı
        X = df[feature_columns]
        y = df["price_usd"]

        # Yeni veri için DataFrame oluştur
        new_data = pd.DataFrame(
            [
                {
                    "ram": ram,
                    "storage": storage,
                    "display_size": display_size,
                    "battery": battery,
                    "foldable": foldable,
                    "ppi_density": ppi,
                    "os_encoded": os_encoded,
                    "display_type_encoded": display_type_encoded,
                    "video_resolution_encoded": video_resolution_encoded,
                    "chipset": chipset
                }
            ]
        )

        # XGBoost modeli (ölçeklendirme olmadan - XGBoost tree-based olduğu için gerekli değil)
        model = xgb.XGBRegressor(
            objective="reg:squarederror",
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42
        )
        
        model.fit(X, y)

        # Tahmin yap
        prediction_price = model.predict(new_data)[0]

        print(f"Predicted price: {round(prediction_price, 2)}")
        print(
            f"Input encodings - OS: {os_encoded}, Display: {display_type_encoded}, Resolution: {video_resolution_encoded}"
        )

        return Response(
            {
                "message": "XGBoost prediction successful",
                "price": round(prediction_price, 2),
                "encodings": {
                    "os": os_encoded,
                    "display_type": display_type_encoded,
                    "video_resolution": video_resolution_encoded,
                },
                "model_info": {
                    "algorithm": "XGBoost",
                    "estimators": 100
                }
            }
        )

    except Exception as e:
        print(f"Error in XGBoost prediction: {str(e)}")
        return Response({"error": str(e)}, status=400)

@api_view(['POST'])
def predict_product_lstm(request):
    product_name = request.data.get('product')

    if not product_name:
        return Response({"error": "Lütfen 'product' alanını POST verisinde gönderin."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        df = pd.read_csv(r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\csv\akakce.csv")

        df["Price"] = df["Price"].apply(lambda x: int(str(x).replace(" TL", "").split(",")[0].replace(".", "")))
        df["Price"] = df["Price"].astype(int)
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])

        product_df = df[df["Product Name"] == product_name].sort_values("Date")

        if len(product_df) < 20:
            return Response({"error": f"Yetersiz veri: {product_name}"}, status=status.HTTP_400_BAD_REQUEST)

        prices = product_df["Price"].values.reshape(-1, 1)
        scaler = MinMaxScaler()
        prices_scaled = scaler.fit_transform(prices)

        look_back = 5

        x, y = [], []
        for i in range(len(prices_scaled) - look_back):
            x.append(prices_scaled[i:i+look_back])
            y.append(prices_scaled[i+look_back])

        x = np.array(x)
        y = np.array(y)

        model = Sequential()
        model.add(LSTM(64, input_shape=(look_back, 1)))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(x, y, epochs=20, batch_size=4, verbose=0)


        input_seq = prices_scaled[-look_back:]
        input_seq = input_seq.reshape((1, look_back, 1))

        forecast_scaled = []
        for _ in range(15):
            pred = model.predict(input_seq)[0]
            forecast_scaled.append(pred[0])
            input_seq = np.append(input_seq[:, 1:, :], [[[pred[0]]]], axis=1)

        forecast = scaler.inverse_transform(np.array(forecast_scaled).reshape(-1, 1)).flatten().tolist()

        return Response({
            "product": product_name,
            "forecast": forecast
        })

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)