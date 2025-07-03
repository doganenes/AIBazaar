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

            current_dir = os.path.dirname(os.path.abspath(__file__))  
            api_dir = os.path.dirname(current_dir)                   
            ai_bazaar_dir = os.path.dirname(api_dir)                 
            ai_dir = os.path.dirname(ai_bazaar_dir)                  

            data_path = os.path.join(ai_dir, "utils", "notebooks", "Product.csv")
            similar_phones = self.find_similar(
                input_data, prediction, data_path
            )

            return {
                "message": "Kaydedilmiş model ile tahmin başarılı",
                "price": round(prediction, 2),
                "recommendations": {
                    "similar_phones": similar_phones,
                    "recommendation_count": len(similar_phones),
                    "recommendation_criteria": {
                        "price_range": f"±25% ({round(prediction * 0.75, 2)} - {round(prediction * 1.25, 2)})",
                        "flexibility": "Weighted similarity scoring with advanced features",
                    },
                },
            }
        
            

        except Exception as e:
            print("Prediction error:", e)
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)
    
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

