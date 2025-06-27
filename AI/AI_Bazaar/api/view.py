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
import os
import traceback
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    VotingRegressor,
)
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib
import pickle
from scipy import stats
from scipy import stats
import warnings
import joblib  
import pickle 
from datetime import datetime
warnings.filterwarnings("ignore")
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
import pandas as pd
import traceback
from trainers.lstm_predictor import LSTMPredictor

def advanced_feature_engineering(df):
    """Gelişmiş özellik mühendisliği ile R2 skorunu artırma"""

    # Temel kombinasyonlar
    df["ram_storage"] = df["ram"] * df["storage"]
    df["battery_display_ratio"] = df["battery"] / (
        df["display_size"] + 0.1
    )  # 0 bölme hatası önleme
    df["ppi_refresh"] = df["ppi_density"] * df["refresh_rate"]
    df["chipset_5g"] = df["chipset"] * (df["5g"] + 1)  # 5G olmayanlarda 0 çarpım önleme

    # Yeni güçlü özellikler
    df["performance_score"] = (df["ram"] * df["chipset"] * df["refresh_rate"]) / 1000
    df["premium_score"] = (
        df["camera"] * df["ppi_density"] * df["refresh_rate"]
    ) / 10000
    df["storage_efficiency"] = df["storage"] / (df["ram"] + 1)
    df["display_quality"] = (
        df["ppi_density"] * df["display_size"] * df["refresh_rate"] / 1000
    )
    df["battery_efficiency"] = df["battery"] / df["display_size"]

    # Kategorik özellikler
    df["is_android"] = (
        df["os_type"].str.contains("Android", case=False, na=False)
    ).astype(int)
    df["is_ios"] = (df["os_type"].str.contains("Ios", case=False, na=False)).astype(int)
    df["is_oled"] = (
        df["display_type"].str.contains("Oled", case=False, na=False)
    ).astype(int)
    df["is_amoled"] = (
        df["display_type"].str.contains("Amoled", case=False, na=False)
    ).astype(int)

    # Logaritmik dönüşümler (fiyat dağılımını normalleştirmek için)
    df["log_battery"] = np.log1p(df["battery"])
    df["log_ram"] = np.log1p(df["ram"])
    df["log_storage"] = np.log1p(df["storage"])
    df["log_camera"] = np.log1p(df["camera"])

    # Çok boyutlu etkileşimler
    df["flagship_indicator"] = (
        (df["ram"] >= 8)
        & (df["storage"] >= 128)
        & (df["camera"] >= 48)
        & (df["5g"] == 1)
    ).astype(int)
    df["budget_indicator"] = ((df["ram"] <= 4) & (df["storage"] <= 64)).astype(int)
    df["mid_range_indicator"] = (
        (df["ram"].between(4, 8)) & (df["storage"].between(64, 256))
    ).astype(int)

    # Teknoloji yılı tahmini (chipset bazında)
    df["tech_generation"] = np.where(
        df["chipset"] <= 14,
        0,  # Eski teknoloji
        np.where(
            df["chipset"] <= 7, 1, np.where(df["chipset"] <= 5, 2, 3)  # Orta teknoloji
        ),
    )  # Yeni teknoloji

    # Koruma özellikleri
    if "waterproof" in df.columns and "dustproof" in df.columns:
        df["protection_score"] = df["waterproof"] + df["dustproof"]
        df["full_protection"] = (
            (df["waterproof"] == 1) & (df["dustproof"] == 1)
        ).astype(int)
    else:
        df["protection_score"] = 0
        df["full_protection"] = 0

    # Fiyat segmentleri (eğitim sırasında kullanmak için)
    if "price" in df.columns:
        df["price_segment"] = pd.qcut(
            df["price"], q=4, labels=["Budget", "Mid", "Premium", "Flagship"]
        )

    return df


def remove_outliers(df, columns, method="iqr"):
    """Aykırı değerleri temizleme"""
    df_clean = df.copy()

    for col in columns:
        if col in df_clean.columns:
            if method == "iqr":
                Q1 = df_clean[col].quantile(0.25)
                Q3 = df_clean[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                df_clean = df_clean[
                    (df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)
                ]
            elif method == "zscore":
                z_scores = np.abs(stats.zscore(df_clean[col]))
                df_clean = df_clean[z_scores < 3]

    return df_clean


def find_similar_phones(df, predicted_price, user_os, user_specs, top_n=5):
    """Geliştirilmiş benzer telefon bulma algoritması"""

    price_tolerance = 0.25  # Toleransı biraz artırdık
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

        # Ağırlıklandırılmış benzerlik skorları
        weights = {
            "ram": 25,
            "storage": 20,
            "display_size": 15,
            "battery": 15,
            "camera": 12,
            "chipset": 10,
            "5g": 8,
            "refresh_rate": 5,
            "price": 20,
        }

        for spec, weight in weights.items():
            if spec in user_specs and spec in row.index:
                if user_specs[spec] != 0:  # 0 bölme hatası önleme
                    diff = abs(row[spec] - user_specs[spec]) / user_specs[spec]
                    if diff <= 0.2:
                        score += weight
                    elif diff <= 0.5:
                        score += weight * 0.7
                    elif diff <= 1.0:
                        score += weight * 0.3

        # Fiyat benzerliği (özel ağırlık)
        if predicted_price != 0:
            price_diff = abs(row["price"] - predicted_price) / predicted_price
            if price_diff <= 0.1:
                score += 25
            elif price_diff <= 0.2:
                score += 15
            elif price_diff <= 0.3:
                score += 8

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
                "product_id": phone.get("ProductID", "N/A"),
            }
        )

    return recommendations


def save_model_and_preprocessors(model, le_os, le_display, feature_columns, model_info):
    """Modeli ve tüm preprocessing bileşenlerini kaydetme"""

    # Kayıt dizini oluştur
    save_dir = "models"
    os.makedirs(save_dir, exist_ok=True)

    # Zaman damgası ile dosya adı
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Model ve preprocessing bileşenlerini içeren sözlük
    model_package = {
        "model": model,
        "label_encoder_os": le_os,
        "label_encoder_display": le_display,
        "feature_columns": feature_columns,
        "model_info": model_info,
        "timestamp": timestamp,
        "version": "1.0",
    }

    # Joblib ile kaydet (önerilen)
    joblib_path = os.path.join(save_dir, f"phone_price_model_{timestamp}.pkl")
    joblib.dump(model_package, joblib_path)

    # Pickle ile de kaydet (alternatif)
    pickle_path = os.path.join(save_dir, f"phone_price_model_{timestamp}_pickle.pkl")
    with open(pickle_path, "wb") as f:
        pickle.dump(model_package, f)

    return joblib_path, pickle_path


def load_model_package(model_path):
    """Kaydedilmiş model paketini yükleme"""
    try:
        # Joblib ile yükle
        if model_path.endswith(".pkl") and "pickle" not in model_path:
            model_package = joblib.load(model_path)
        else:
            # Pickle ile yükle
            with open(model_path, "rb") as f:
                model_package = pickle.load(f)

        return model_package
    except Exception as e:
        print(f"Model yükleme hatası: {e}")
        return None


@api_view(["POST"])
def train_and_save_model(request):
    try:
        # Veri yükleme
        csv_path = request.data.get(
            "csv_path",
            r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\notebooks\Product.csv",
        )
        df = pd.read_csv(csv_path)

        # Sütun adlarını yeniden adlandırma
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

        # Veri temizleme
        df["os_type"] = df["os_type"].str.strip().str.title()
        df["display_type"] = (
            df["display_type"].str.strip().str.split(",").str[0].str.title()
        )

        # Eksik sütunları ekleme
        if "waterproof" not in df.columns:
            df["waterproof"] = 0
        if "dustproof" not in df.columns:
            df["dustproof"] = 0

        # Numerik dönüşüm
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

        # NaN değerleri temizleme
        df = df.dropna(subset=numeric_columns)

        if len(df) < 10:
            return Response(
                {"error": "Insufficient clean data for training"}, status=400
            )

        # Aykırı değer temizleme
        outlier_columns = ["price"]
        if len(df) >= 200:
            df_clean = remove_outliers(df, outlier_columns, method="iqr")
        else:
            df_clean = df.copy()

        # Gelişmiş özellik mühendisliği
        df_clean = advanced_feature_engineering(df_clean)

        # OS tipi için fiyat bazlı ordinal encoding
        os_price_means = df_clean.groupby("os_type")["price"].mean()
        df_clean["os_encoded"] = df_clean["os_type"].map(os_price_means)

        # Display tipi için LabelEncoder
        le_display = LabelEncoder()
        df_clean["display_encoded"] = le_display.fit_transform(df_clean["display_type"])

        # Özellik seçimi
        feature_columns = [
            # Temel özellikler
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
            # Mühendislik özellikleri
            "ram_storage",
            "battery_display_ratio",
            "ppi_refresh",
            "chipset_5g",
            "performance_score",
            "premium_score",
            "storage_efficiency",
            "display_quality",
            "battery_efficiency",
            # Kategorik özellikler (ordinal olarak os_encoded, label encoded display_encoded)
            "os_encoded",
            "display_encoded",
            # Logaritmik özellikler
            "log_battery",
            "log_ram",
            "log_storage",
            "log_camera",
            # Segment özellikleri
            "flagship_indicator",
            "budget_indicator",
            "mid_range_indicator",
            "tech_generation",
            "protection_score",
            "full_protection",
        ]

        X = df_clean[feature_columns].copy()
        y = df_clean["price"]

        # Ensemble Model
        rf_model = RandomForestRegressor(
            n_estimators=500,
            max_depth=None,
            min_samples_split=5,
            min_samples_leaf=2,
            max_features="sqrt",
            bootstrap=True,
            random_state=42,
            n_jobs=-1,
        )

        gb_model = GradientBoostingRegressor(
            n_estimators=400,
            max_depth=6,
            learning_rate=0.08,
            subsample=0.85,
            min_samples_split=10,
            min_samples_leaf=5,
            random_state=42,
            validation_fraction=0.15,
            n_iter_no_change=25,
            tol=1e-4,
        )

        model = VotingRegressor([("rf", rf_model), ("gb", gb_model)], n_jobs=-1)

        # Cross-validation
        cv_folds = min(10, max(3, len(df_clean) // 15))
        cv = KFold(n_splits=cv_folds, shuffle=True, random_state=42)

        scoring_metrics = ["r2", "neg_mean_squared_error", "neg_mean_absolute_error"]
        cv_results = {}

        for metric in scoring_metrics:
            scores = cross_val_score(model, X, y, scoring=metric, cv=cv, n_jobs=-1)
            cv_results[metric] = {"mean": np.mean(scores), "std": np.std(scores)}

        mean_r2 = round(cv_results["r2"]["mean"], 4)
        std_r2 = round(cv_results["r2"]["std"], 4)

        # Model eğitimi
        model.fit(X, y)

        # Eğitim verisi üzerinde performans
        y_pred_train = model.predict(X)
        train_r2 = r2_score(y, y_pred_train)
        train_mae = mean_absolute_error(y, y_pred_train)
        train_rmse = np.sqrt(mean_squared_error(y, y_pred_train))

        # Model bilgileri
        model_info = {
            "cv_r2_mean": mean_r2,
            "cv_r2_std": std_r2,
            "train_r2": train_r2,
            "train_mae": train_mae,
            "train_rmse": train_rmse,
            "data_samples": len(df_clean),
            "feature_count": len(feature_columns),
            "cv_folds": cv_folds,
        }
        joblib_path, pickle_path = save_model_and_preprocessors(
            model, os_price_means, le_display, feature_columns, model_info
        )
        return Response(
            {
                "message": "Model başarıyla eğitildi ve kaydedildi",
                "model_paths": {"joblib": joblib_path, "pickle": pickle_path},
                "model_performance": {
                    "cross_validation_r2": f"{mean_r2:.4f} ± {std_r2:.4f}",
                    "training_r2": f"{train_r2:.4f}",
                    "mae": f"{train_mae:.2f}",
                    "rmse": f"{train_rmse:.2f}",
                },
                "data_info": {
                    "original_samples": len(df),
                    "cleaned_samples": len(df_clean),
                    "features_used": len(feature_columns),
                },
            }
        )

    except Exception as e:
        traceback.print_exc()
        return Response({"error": str(e)}, status=400)


@api_view(["POST"])
def predict_product_rf(
    request,
    model_path=r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\models\phone_price_model_20250624_200303.pkl",
):
    """Kaydedilmiş modeli kullanarak tahmin yap"""
    try:
        model_path = request.data.get("model_path", model_path)
        if not model_path or not os.path.exists(model_path):
            return Response({"error": "Model dosyası bulunamadı"}, status=400)

        # Modeli yükle
        model_package = load_model_package(model_path)
        if not model_package:
            return Response({"error": "Model yüklenemedi"}, status=400)

        # Model bileşenlerini çıkar
        model = model_package["model"]
        os_price_means = model_package[
            "label_encoder_os"
        ]  # Burada artık LabelEncoder değil, os fiyat ortalamaları
        le_display = model_package["label_encoder_display"]
        feature_columns = model_package["feature_columns"]
        model_info = model_package["model_info"]

        # Kullanıcı verileri
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
        is_5g = int(data.get("5G"))
        refresh_rate = int(data.get("Refresh Rate", 60))
        waterproof = int(data.get("Waterproof", 0))
        dustproof = int(data.get("Dustproof", 0))

        # Yeni veri hazırlama
        new_data = pd.DataFrame(
            [
                {
                    "ram": ram,
                    "storage": storage,
                    "display_size": display_size,
                    "battery": battery,
                    "ppi_density": ppi,
                    "os_type": os_name,
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

        new_data = advanced_feature_engineering(new_data)

        # OS encoding - ortalama fiyatları kullanarak map yapıyoruz
        try:
            new_data["os_encoded"] = new_data["os_type"].map(os_price_means)
            if new_data["os_encoded"].isnull().any():
                missing = new_data.loc[
                    new_data["os_encoded"].isnull(), "os_type"
                ].unique()
                return Response(
                    {"error": f"Bilinmeyen OS türü(leri): {', '.join(missing)}"},
                    status=400,
                )
        except Exception as ex:
            return Response({"error": f"OS encoding hatası: {str(ex)}"}, status=400)

        # Display encoding (LabelEncoder olduğu için transform kullanıyoruz)
        try:
            new_data["display_encoded"] = le_display.transform(new_data["display_type"])
        except ValueError:
            return Response(
                {"error": f"Bilinmeyen display türü: {display_type}"}, status=400
            )
        df = pd.read_csv(
            r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\notebooks\Product.csv"
        )
        prediction = model.predict(new_data[feature_columns])[0]
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
        df["os_type"] = df["os_type"].str.strip().str.title()
        df["display_type"] = (
            df["display_type"].str.strip().str.split(",").str[0].str.title()
        )

        if "waterproof" not in df.columns:
            df["waterproof"] = 0
        if "dustproof" not in df.columns:
            df["dustproof"] = 0
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        df_clean = df.dropna(subset=numeric_columns)

        df_clean = advanced_feature_engineering(df_clean)

        user_specs = {
            "ram": ram,
            "storage": storage,
            "display_size": display_size,
            "battery": battery,
            "camera": camera,
            "chipset": chipset,
            "5g": is_5g,
            "refresh_rate": refresh_rate,
        }

        similar_phones = find_similar_phones(
            df_clean, prediction, os_name, user_specs, top_n=3
        )
       

        return Response(
            {
                "message": "Kaydedilmiş model ile tahmin başarılı",
                "price": round(prediction, 2),
                "model_info": model_info,
                "model_path": model_path,
                "model_version": model_package.get("version", "Unknown"),
                "model_timestamp": model_package.get("timestamp", "Unknown"),
                "recommendations": {
                    "similar_phones": similar_phones,
                    "recommendation_count": len(similar_phones),
                    "recommendation_criteria": {
                        "price_range": f"±25% ({round(prediction * 0.75, 2)} - {round(prediction * 1.25, 2)})",
                        "os_restriction": f"Only {os_name} phones",
                        "flexibility": "Weighted similarity scoring with advanced features",
                    },
                },
            }
        )

    except Exception as e:
        traceback.print_exc()
        return Response({"error": str(e)}, status=400)


@api_view(["POST"])
def predict_with_lstm_model(request):
    try:
        data = request.data
        product_id = int(data.get("product_id"))
        model_dir = data.get("model_dir", r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\AI_Bazaar\trainers\product_models")

        if not product_id:
            return Response({"error": "product_id parametresi zorunludur"}, status=400)

        model_path = os.path.join(model_dir, f"{product_id}_model.h5")
        scalers_path = os.path.join(model_dir, f"{product_id}_scalers.pkl")

        if not os.path.exists(model_path):
            return Response({"error": f"Ürün {product_id} için model bulunamadı"}, status=404)
        if not os.path.exists(scalers_path):
            return Response({"error": f"Ürün {product_id} için scaler bulunamadı"}, status=404)

        predictor = LSTMPredictor(model_path, scalers_path)
        if not predictor.load_model_and_scalers():
            return Response({"error": "Model veya scaler yüklenemedi"}, status=500)

        data_path = data.get("data_path", r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\notebooks\LSTMPriceHistory.csv")
        if not os.path.exists(data_path):
            return Response({"error": "Veri dosyası bulunamadı"}, status=404)

        df = pd.read_csv(data_path, low_memory=False)
        df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
        df["CurrencyRate"] = pd.to_numeric(df["CurrencyRate"], errors="coerce")
        df["RecordDate"] = pd.to_datetime(df["RecordDate"], errors="coerce")
        df = df.dropna(subset=["RecordDate", "Price", "CurrencyRate"])

        product_df = df[df["ProductID"] == product_id].sort_values("RecordDate")
        if product_df.empty:
            return Response({"error": f"Ürün {product_id} için veri bulunamadı"}, status=404)

        if len(product_df) < predictor.look_back:
            return Response({
                "error": f"En az {predictor.look_back} günlük veri gerekli, mevcut: {len(product_df)}"
            }, status=400)

        product_df = predictor.create_features_for_prediction(product_df)

        feature_cols = [
            "Price", "CurrencyRate", "day_of_week", "is_holiday",
            "price_lag_1", "price_lag_3", "currency_lag_1",
            "price_rolling_mean_7", "price_rolling_std_7"
        ]

        features_scaled = predictor.scale_features_for_prediction(product_df, feature_cols)
        sequence = predictor.prepare_sequence_for_prediction(features_scaled)

        predicted_prices = predictor.predict_next_15_days(sequence)

        actuals = product_df["Price"].values[-15:]
        preds = np.array(predicted_prices[:len(actuals)])

        if len(actuals) == len(preds):
            mae = float(np.mean(np.abs(preds - actuals)))
            mape = float(np.mean(np.abs((preds - actuals) / actuals))) * 100
            rmse = float(np.sqrt(np.mean((preds - actuals) ** 2)))
            ss_res = np.sum((actuals - preds) ** 2)
            ss_tot = np.sum((actuals - np.mean(actuals)) ** 2)
            r2 = float(1 - ss_res / ss_tot) if ss_tot != 0 else 0.0
        else:
            mae = mape = rmse = r2 = None

        return Response({
            "product": product_df['ProductName'].iloc[0],
            "productId": int(product_id),
            "steps": 15,
            "predicted_prices": [round(float(p), 2) for p in predicted_prices],
            "metrics": {
                "mae": round(mae, 2) if mae is not None else None,
                "mape": round(mape, 2) if mape is not None else None,
                "rmse": round(rmse, 2) if rmse is not None else None,
            },
            "features_used": feature_cols
        })

    except Exception as e:
        traceback.print_exc()
        return Response({
            "error": f"Tahmin sırasında hata oluştu: {str(e)}",
            "success": False
        }, status=500)

