import os
import numpy as np
import pandas as pd
import joblib
import pickle
import traceback
from datetime import datetime
from scipy import stats
from sklearn.preprocessing import LabelEncoder
import warnings
import os
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
warnings.filterwarnings("ignore")


class PhonePricePredictor:
    def __init__(self, model_path=None):
        self.model_path = model_path
        self.model = None
        self.feature_columns = None
        self.model_info = None
        self.label_encoder_os = None
        self.label_encoder_display = None
        self.model_package = None

        if model_path:
            self.load_model(model_path)

    def load_model(self, model_path:str):
        try:
            if model_path.endswith(".pkl") and "pickle" not in model_path:
                self.model_package = joblib.load(model_path)
            else:
                with open(model_path, "rb") as f:
                    self.model_package = pickle.load(f)

            self.model = self.model_package["model"]
            self.label_encoder_os = self.model_package["label_encoder_os"]
            self.label_encoder_display = self.model_package["label_encoder_display"]
            self.feature_columns = self.model_package["feature_columns"]
            self.model_info = self.model_package["model_info"]

        except Exception as e:
            print(f"Model load error: {e}")

    def predict(self, input_data):
        try:
            df_input = pd.DataFrame([input_data])

            df_input = self.advanced_feature_engineering(df_input)
            df_input["os_encoded"] = df_input["os_type"].map(self.label_encoder_os)
            df_input["display_encoded"] = self.label_encoder_display.transform(
                df_input["display_type"]
            )

            prediction = self.model.predict(df_input[self.feature_columns])[0]

            similar_phones = self.find_similar(
                input_data, prediction, r"C:\Users\pc\Desktop\AIBazaar2\AIBazaar\AI\utils\notebooks\Product.csv"
            )

            return {
                "predicted_price": round(prediction, 2),
                "similar_phones": similar_phones
            }

        except Exception as e:
            print("Prediction error:", e)
            traceback.print_exc()
            return {"error": str(e)}


    def find_similar(self, input_data, predicted_price, dataset_path, top_n=5):
        df = pd.read_csv(dataset_path)
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

        df = self.advanced_feature_engineering(df)

        return self.find_similar_phones(
            df, predicted_price, input_data["os_type"], input_data, top_n
        )

    def find_similar_phones(self, df, predicted_price, user_os, user_specs, top_n=5):
        price_tolerance = 0.25
        min_price = predicted_price * (1 - price_tolerance)
        max_price = predicted_price * (1 + price_tolerance)

        os_filter = df["os_type"].str.contains(user_os, case=False, na=False)

        similar_phones = df[
            (df["price"] >= min_price) & (df["price"] <= max_price) & os_filter
        ].copy()

        if similar_phones.empty:
            return []

        def calculate_score(row):
            score = 0
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
                if spec in user_specs:
                    diff = abs(row[spec] - user_specs[spec]) / max(user_specs[spec], 1)
                    if diff <= 0.2:
                        score += weight
                    elif diff <= 0.5:
                        score += weight * 0.7
                    elif diff <= 1.0:
                        score += weight * 0.3

            return score

        similar_phones["similarity_score"] = similar_phones.apply(
            calculate_score, axis=1
        )
        return (
            similar_phones.sort_values("similarity_score", ascending=False)
            .head(top_n)
            .to_dict(orient="records")
        )

    def advanced_feature_engineering(self, df):
        df["ram_storage"] = df["ram"] * df["storage"]
        df["battery_display_ratio"] = df["battery"] / (df["display_size"] + 0.1)
        df["ppi_refresh"] = df["ppi_density"] * df["refresh_rate"]
        df["chipset_5g"] = df["chipset"] * (df["5g"] + 1)
        df["performance_score"] = (
            df["ram"] * df["chipset"] * df["refresh_rate"]
        ) / 1000
        df["premium_score"] = (
            df["camera"] * df["ppi_density"] * df["refresh_rate"]
        ) / 10000
        df["storage_efficiency"] = df["storage"] / (df["ram"] + 1)
        df["display_quality"] = (
            df["ppi_density"] * df["display_size"] * df["refresh_rate"] / 1000
        )
        df["battery_efficiency"] = df["battery"] / df["display_size"]

        df["is_android"] = (
            df["os_type"].str.contains("Android", case=False, na=False)
        ).astype(int)
        df["is_ios"] = (df["os_type"].str.contains("Ios", case=False, na=False)).astype(
            int
        )
        df["is_oled"] = (
            df["display_type"].str.contains("Oled", case=False, na=False)
        ).astype(int)
        df["is_amoled"] = (
            df["display_type"].str.contains("Amoled", case=False, na=False)
        ).astype(int)

        df["log_battery"] = np.log1p(df["battery"])
        df["log_ram"] = np.log1p(df["ram"])
        df["log_storage"] = np.log1p(df["storage"])
        df["log_camera"] = np.log1p(df["camera"])

        df["flagship_indicator"] = (
            (df["ram"] >= 8)
            & (df["storage"] >= 128)
            & (df["camera"] >= 48)
            & (df["5g"] == 1)
        ).astype(int)

        df["budget_indicator"] = ((df["ram"] <= 4) & (df["storage"] <= 64)).astype(int)

        df["mid_range_indicator"] = (
            df["ram"].between(4, 8) & df["storage"].between(64, 256)
        ).astype(int)

        df["tech_generation"] = np.where(
            df["chipset"] <= 14,
            0,
            np.where(df["chipset"] <= 7, 1, np.where(df["chipset"] <= 5, 2, 3)),
        )

        if "waterproof" in df.columns and "dustproof" in df.columns:
            df["protection_score"] = df["waterproof"] + df["dustproof"]
            df["full_protection"] = (
                (df["waterproof"] == 1) & (df["dustproof"] == 1)
            ).astype(int)
        else:
            df["protection_score"] = 0
            df["full_protection"] = 0

        return df


# def predict_with_saved_model(
#     request,
#     model_path=r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\models\phone_price_model_20250624_200303.pkl",
# ):
#     """Kaydedilmiş modeli kullanarak tahmin yap"""
#     try:
#         model_path = request.data.get("model_path", model_path)
#         if not model_path or not os.path.exists(model_path):
#             return

#         # Modeli yükle
#         model_package = load_model_package(model_path)
#         if not model_package:
#             return

#         # Model bileşenlerini çıkar
#         model = model_package["model"]
#         os_price_means = model_package[
#             "label_encoder_os"
#         ]  # Burada artık LabelEncoder değil, os fiyat ortalamaları
#         le_display = model_package["label_encoder_display"]
#         feature_columns = model_package["feature_columns"]
#         model_info = model_package["model_info"]

#         # Kullanıcı verileri
#         data = request.data
#         ram = float(data.get("RAM"))
#         storage = float(data.get("Storage"))
#         display_size = float(data.get("Display Size"))
#         battery = float(data.get("Battery Capacity"))
#         ppi = int(data.get("Pixel Density"))
#         os_name = data.get("Operating System").strip().title()
#         display_type = data.get("Display Technology").strip().split(",")[0].title()
#         camera = float(data.get("camera"))
#         chipset = int(data.get("CPU Manufacturing"))
#         is_5g = int(data.get("5G"))
#         refresh_rate = int(data.get("Refresh Rate", 60))
#         waterproof = int(data.get("Waterproof", 0))
#         dustproof = int(data.get("Dustproof", 0))

#         # Yeni veri hazırlama
#         new_data = pd.DataFrame(
#             [
#                 {
#                     "ram": ram,
#                     "storage": storage,
#                     "display_size": display_size,
#                     "battery": battery,
#                     "ppi_density": ppi,
#                     "os_type": os_name,
#                     "display_type": display_type,
#                     "camera": camera,
#                     "chipset": chipset,
#                     "5g": is_5g,
#                     "refresh_rate": refresh_rate,
#                     "waterproof": waterproof,
#                     "dustproof": dustproof,
#                 }
#             ]
#         )

#         new_data = advanced_feature_engineering(new_data)

#         # OS encoding - ortalama fiyatları kullanarak map yapıyoruz
#         try:
#             new_data["os_encoded"] = new_data["os_type"].map(os_price_means)
#             if new_data["os_encoded"].isnull().any():
#                 missing = new_data.loc[
#                     new_data["os_encoded"].isnull(), "os_type"
#                 ].unique()
#                 return

#         except Exception as ex:
#             return

#         # Display encoding (LabelEncoder olduğu için transform kullanıyoruz)
#         try:
#             new_data["display_encoded"] = le_display.transform(new_data["display_type"])
#         except ValueError:
#             return

#         df = pd.read_csv(
#             r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\notebooks\Product.csv"
#         )
#         prediction = model.predict(new_data[feature_columns])[0]
#         df.rename(
#             columns={
#                 "RAM": "ram",
#                 "Internal Storage": "storage",
#                 "Display Size": "display_size",
#                 "Battery Capacity": "battery",
#                 "Pixel Density": "ppi_density",
#                 "Operating System": "os_type",
#                 "Display Technology": "display_type",
#                 "Camera Resolution": "camera",
#                 "CPU Manufacturing": "chipset",
#                 "Price": "price",
#                 "5G": "5g",
#                 "Model": "phone_model",
#                 "Refresh Rate": "refresh_rate",
#                 "Waterproof": "waterproof",
#                 "Dustproof": "dustproof",
#             },
#             inplace=True,
#         )
#         # numeric_columns = [
#         #     "ram",
#         #     "storage",
#         #     "display_size",
#         #     "battery",
#         #     "ppi_density",
#         #     "camera",
#         #     "chipset",
#         #     "5g",
#         #     "refresh_rate",
#         #     "waterproof",
#         #     "dustproof",
#         #     "price",
#         # ]
#         df["os_type"] = df["os_type"].str.strip().str.title()
#         df["display_type"] = (
#             df["display_type"].str.strip().str.split(",").str[0].str.title()
#         )

#         # if "waterproof" not in df.columns:
#         #     df["waterproof"] = 0
#         # if "dustproof" not in df.columns:
#         #     df["dustproof"] = 0
#         # for col in numeric_columns:
#         #     if col in df.columns:
#         #         df[col] = pd.to_numeric(df[col], errors="coerce")
#         # df_clean = df.dropna(subset=numeric_columns)

#         # df_clean = advanced_feature_engineering(df_clean)

#         user_specs = {
#             "ram": ram,
#             "storage": storage,
#             "display_size": display_size,
#             "battery": battery,
#             "camera": camera,
#             "chipset": chipset,
#             "5g": is_5g,
#             "refresh_rate": refresh_rate,
#         }

#         similar_phones = find_similar_phones(
#             df, prediction, os_name, user_specs, top_n=3
#         )

#         return {
#             "message": "Kaydedilmiş model ile tahmin başarılı",
#             "price": round(prediction, 2),
#             "model_info": model_info,
#             "model_path": model_path,
#             "model_version": model_package.get("version", "Unknown"),
#             "model_timestamp": model_package.get("timestamp", "Unknown"),
#             "recommendations": {
#                 "similar_phones": similar_phones,
#                 "recommendation_count": len(similar_phones),
#                 "recommendation_criteria": {
#                     "price_range": f"±25% ({round(prediction * 0.75, 2)} - {round(prediction * 1.25, 2)})",
#                     "os_restriction": f"Only {os_name} phones",
#                     "flexibility": "Weighted similarity scoring with advanced features",
#                 },
#             },
#         }

#     except Exception as e:
#         traceback.print_exc()
#         return

# def train_and_save_model():
#     try:
#         csv_path = r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\notebooks\Product.csv"
#         df = pd.read_csv(csv_path)

#         df.rename(
#             columns={
#                 "RAM": "ram",
#                 "Internal Storage": "storage",
#                 "Display Size": "display_size",
#                 "Battery Capacity": "battery",
#                 "Pixel Density": "ppi_density",
#                 "Operating System": "os_type",
#                 "Display Technology": "display_type",
#                 "Camera Resolution": "camera",
#                 "CPU Manufacturing": "chipset",
#                 "Price": "price",
#                 "5G": "5g",
#                 "Model": "phone_model",
#                 "Refresh Rate": "refresh_rate",
#                 "Waterproof": "waterproof",
#                 "Dustproof": "dustproof",
#             },
#             inplace=True,
#         )

#         df["os_type"] = df["os_type"].str.strip().str.title()
#         df["display_type"] = (
#             df["display_type"].str.strip().str.split(",").str[0].str.title()
#         )

#         if "waterproof" not in df.columns:
#             df["waterproof"] = 0
#         if "dustproof" not in df.columns:
#             df["dustproof"] = 0

#         numeric_columns = [
#             "ram",
#             "storage",
#             "display_size",
#             "battery",
#             "ppi_density",
#             "camera",
#             "chipset",
#             "5g",
#             "refresh_rate",
#             "waterproof",
#             "dustproof",
#             "price",
#         ]

#         for col in numeric_columns:
#             if col in df.columns:
#                 df[col] = pd.to_numeric(df[col], errors="coerce")

#         df = df.dropna(subset=numeric_columns)

#         if len(df) < 10:
#             return 

#         outlier_columns = ["price"]
#         if len(df) >= 200:
#             df_clean = remove_outliers(df, outlier_columns, method="iqr")
#         else:
#             df_clean = df.copy()

#         df_clean = advanced_feature_engineering(df_clean)

#         os_price_means = df_clean.groupby("os_type")["price"].mean()
#         df_clean["os_encoded"] = df_clean["os_type"].map(os_price_means)

#         le_display = LabelEncoder()
#         df_clean["display_encoded"] = le_display.fit_transform(df_clean["display_type"])

#         feature_columns = [
#             "ram",
#             "storage",
#             "display_size",
#             "battery",
#             "ppi_density",
#             "camera",
#             "chipset",
#             "5g",
#             "refresh_rate",
#             "waterproof",
#             "dustproof",
#             "ram_storage",
#             "battery_display_ratio",
#             "ppi_refresh",
#             "chipset_5g",
#             "performance_score",
#             "premium_score",
#             "storage_efficiency",
#             "display_quality",
#             "battery_efficiency",
#             "os_encoded",
#             "display_encoded",
#             "log_battery",
#             "log_ram",
#             "log_storage",
#             "log_camera",
#             "flagship_indicator",
#             "budget_indicator",
#             "mid_range_indicator",
#             "tech_generation",
#             "protection_score",
#             "full_protection",
#         ]

#         X = df_clean[feature_columns].copy()
#         y = df_clean["price"]

#         # Ensemble Model
#         rf_model = RandomForestRegressor(
#             n_estimators=500,
#             max_depth=None,
#             min_samples_split=5,
#             min_samples_leaf=2,
#             max_features="sqrt",
#             bootstrap=True,
#             random_state=42,
#             n_jobs=-1,
#         )

#         gb_model = GradientBoostingRegressor(
#             n_estimators=400,
#             max_depth=6,
#             learning_rate=0.08,
#             subsample=0.85,
#             min_samples_split=10,
#             min_samples_leaf=5,
#             random_state=42,
#             validation_fraction=0.15,
#             n_iter_no_change=25,
#             tol=1e-4,
#         )

#         model = VotingRegressor([("rf", rf_model), ("gb", gb_model)], n_jobs=-1)

#         # Cross-validation
#         cv_folds = min(10, max(3, len(df_clean) // 15))
#         cv = KFold(n_splits=cv_folds, shuffle=True, random_state=42)

#         scoring_metrics = ["r2", "neg_mean_squared_error", "neg_mean_absolute_error"]
#         cv_results = {}

#         for metric in scoring_metrics:
#             scores = cross_val_score(model, X, y, scoring=metric, cv=cv, n_jobs=-1)
#             cv_results[metric] = {"mean": np.mean(scores), "std": np.std(scores)}

#         mean_r2 = round(cv_results["r2"]["mean"], 4)
#         std_r2 = round(cv_results["r2"]["std"], 4)

#         model.fit(X, y)

#         y_pred_train = model.predict(X)
#         train_r2 = r2_score(y, y_pred_train)
#         train_mae = mean_absolute_error(y, y_pred_train)
#         train_rmse = np.sqrt(mean_squared_error(y, y_pred_train))

#         model_info = {
#             "cv_r2_mean": mean_r2,
#             "cv_r2_std": std_r2,
#             "train_r2": train_r2,
#             "train_mae": train_mae,
#             "train_rmse": train_rmse,
#             "data_samples": len(df_clean),
#             "feature_count": len(feature_columns),
#             "cv_folds": cv_folds,
#         }
#         joblib_path, pickle_path = save_model_and_preprocessors(
#             model, os_price_means, le_display, feature_columns, model_info
#         )
#         return (
#             {
#                 "message": "Model başarıyla eğitildi ve kaydedildi",
#                 "model_paths": {"joblib": joblib_path, "pickle": pickle_path},
#                 "model_performance": {
#                     "cross_validation_r2": f"{mean_r2:.4f} ± {std_r2:.4f}",
#                     "training_r2": f"{train_r2:.4f}",
#                     "mae": f"{train_mae:.2f}",
#                     "rmse": f"{train_rmse:.2f}",
#                 },
#                 "data_info": {
#                     "original_samples": len(df),
#                     "cleaned_samples": len(df_clean),
#                     "features_used": len(feature_columns),
#                 },
#             }
#         )

#     except Exception as e:
#         traceback.print_exc()
#         return


# train_and_save_model()
