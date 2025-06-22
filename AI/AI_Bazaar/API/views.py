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
from catboost import CatBoostRegressor
import traceback
model = CatBoostRegressor(iterations=200, learning_rate=0.1, depth=8, verbose=False)

# lstm_trainer = LSTMModelTrainer(
#    data_path=r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\notebooks\LSTMPriceHistory.csv",
#    model_dir=r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\models"
# )

# 1. DAHA İYİ OS ENCODING STRATEJİSİ


# Seçenek 2: Label Encoding + StandardScaler
from sklearn.preprocessing import LabelEncoder, StandardScaler


# 2. İYİLEŞTİRİLMİŞ MODEL EĞİTİMİ


from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold, cross_val_score
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pandas as pd


def feature_engineering(df):
    # Yeni özellikler üret
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

    # Yeni özellikler: waterproof ve dustproof için kombinasyonlar
    if "waterproof" in df.columns and "dustproof" in df.columns:
        df["protection_score"] = df["waterproof"] + df["dustproof"]  # 0-2 arası skor
        df["full_protection"] = (
            (df["waterproof"] == 1) & (df["dustproof"] == 1)
        ).astype(int)

    return df


@api_view(["POST"])
def predict_product_xgboost(request):
    try:
        data = request.data

        # Girdi al
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
        waterproof = int(data.get("Waterproof", 0))  # Default 0 olarak ayarlandı
        dustproof = int(data.get("Dustproof", 0))  # Default 0 olarak ayarlandı

        # Veri seti yükle
        df = pd.read_csv(
            r"C:\Users\pc\Desktop\AIbazaar\AIBazaar\AI\utils\notebooks\Product.csv"
        )

        # Kolonları düzelt
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
                "Waterproof": "waterproof",  # Yeni sütun
                "Dustproof": "dustproof",  # Yeni sütun
            },
            inplace=True,
        )

        # Kategorik temizleme
        df["os_type"] = df["os_type"].str.strip().str.title()
        df["display_type"] = (
            df["display_type"].str.strip().str.split(",").str[0].str.title()
        )

        # Eğer CSV'de waterproof/dustproof sütunları yoksa, varsayılan değerler ekle
        if "waterproof" not in df.columns:
            df["waterproof"] = 0  # Varsayılan olarak waterproof değil
        if "dustproof" not in df.columns:
            df["dustproof"] = 0  # Varsayılan olarak dustproof değil

        # Sayısal sütunlardaki problematik değerleri temizle
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
                # String değerleri NaN'a çevir
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # NaN değerleri olan satırları kaldır
        df = df.dropna(subset=numeric_columns)

        # Veri setinin yeterli büyüklükte olduğunu kontrol et
        if len(df) < 10:
            return Response(
                {"error": "Insufficient clean data for training"}, status=400
            )

        # Feature engineering uygula
        df = feature_engineering(df)

        # Gerekli sütunlar (waterproof ve dustproof eklendi)
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
            "waterproof",  # Yeni özellik
            "dustproof",  # Yeni özellik
            # Mevcut özellikler
            "ram_storage",
            "battery_display_ratio",
            "ppi_refresh",
            "chipset_5g",
            "is_android",
            "is_ios",
            "is_oled",
            "log_battery",
            # Yeni kombinasyon özellikleri
            "protection_score",
            "full_protection",
        ]

        X = df[feature_columns].copy()
        y = df["price"]

        # Label Encoding kategorik değişkenler
        le_os = LabelEncoder()
        X["os_type"] = le_os.fit_transform(X["os_type"])

        le_display = LabelEncoder()
        X["display_type"] = le_display.fit_transform(X["display_type"])

        # Yeni veri
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
                    "waterproof": waterproof,  # Yeni özellik
                    "dustproof": dustproof,  # Yeni özellik
                }
            ]
        )

        # Feature engineering yeni veri için
        new_data = feature_engineering(new_data)

        # Yeni veri için label encoding - hata kontrolü ile
        try:
            new_data["os_type"] = le_os.transform(new_data["os_type"])
        except ValueError:
            # Eğer yeni OS tipi training'de yoksa, en yaygın olan ile değiştir
            most_common_os = df["os_type"].mode()[0]
            new_data["os_type"] = le_os.transform([most_common_os])

        try:
            new_data["display_type"] = le_display.transform(new_data["display_type"])
        except ValueError:
            # Eğer yeni display tipi training'de yoksa, en yaygın olan ile değiştir
            most_common_display = df["display_type"].mode()[0]
            new_data["display_type"] = le_display.transform([most_common_display])

        # Model oluştur
        model = RandomForestRegressor(
            n_estimators=200,
            max_depth=15,
            random_state=42,
            n_jobs=-1,
        )

        # 5-fold CV ile r2 skoru hesapla
        cv = KFold(n_splits=5, shuffle=True, random_state=42)
        scores = cross_val_score(model, X, y, scoring="r2", cv=cv, n_jobs=-1)

        mean_r2 = round(np.mean(scores), 4)
        std_r2 = round(np.std(scores), 4)

        # Modeli tüm veriyle eğit
        model.fit(X, y)

        # Tahmin yap
        prediction = model.predict(new_data)[0]

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
            }
        )

    except Exception as e:
        traceback.print_exc()
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
