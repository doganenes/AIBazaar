import traceback
import os
import traceback
import pickle
from datetime import datetime
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib

from rest_framework.decorators import api_view
from rest_framework.response import Response

from AI.AI_Bazaar.api.views import advanced_feature_engineering
from AI.AI_Bazaar.trainers.train_model import remove_outliers



def save_model_and_preprocessors(model, le_os, le_display, feature_columns, model_info):
    save_dir = "models"
    os.makedirs(save_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    model_package = {
        'model': model,
        'label_encoder_os': le_os,
        'label_encoder_display': le_display,
        'feature_columns': feature_columns,
        'model_info': model_info,
        'timestamp': timestamp,
        'version': '1.0'
    }

    joblib_path = os.path.join(save_dir, f'phone_price_model_{timestamp}.pkl')
    joblib.dump(model_package, joblib_path)
    
    pickle_path = os.path.join(save_dir, f'phone_price_model_{timestamp}_pickle.pkl')
    with open(pickle_path, 'wb') as f:
        pickle.dump(model_package, f)
    
    return joblib_path, pickle_path

def train_and_save_model(request):
    try:
        csv_path = request.data.get("csv_path", r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\notebooks\Product.csv")
        df = pd.read_csv(csv_path)

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

        df = df.dropna(subset=numeric_columns)

        if len(df) < 10:
            return Response({"error": "Insufficient clean data for training"}, status=400)

        outlier_columns = ["price"]
        if len(df) >= 200:
            df_clean = remove_outliers(df, outlier_columns, method='iqr')
        else:
            df_clean = df.copy()

        df_clean = advanced_feature_engineering(df_clean)

        feature_columns = [
            "ram", "storage", "display_size", "battery", "ppi_density", 
            "camera", "chipset", "5g", "refresh_rate", "waterproof", "dustproof",
            
            "ram_storage", "battery_display_ratio", "ppi_refresh", "chipset_5g",
            "performance_score", "premium_score", "storage_efficiency", 
            "display_quality", "battery_efficiency",
            
            "is_android", "is_ios", "is_oled", "is_amoled",
            
            "log_battery", "log_ram", "log_storage", "log_camera",
            
            "flagship_indicator", "budget_indicator", "mid_range_indicator",
            "tech_generation", "protection_score", "full_protection"
        ]

        le_os = LabelEncoder()
        df_clean["os_encoded"] = le_os.fit_transform(df_clean["os_type"])
        le_display = LabelEncoder()
        df_clean["display_encoded"] = le_display.fit_transform(df_clean["display_type"])
        
        feature_columns.extend(["os_encoded", "display_encoded"])

        X = df_clean[feature_columns].copy()
        y = df_clean["price"]

        from sklearn.ensemble import VotingRegressor
        
        rf_model = RandomForestRegressor(
            n_estimators=500,
            max_depth=None,
            min_samples_split=5,
            min_samples_leaf=2,
            max_features='sqrt',
            bootstrap=True,
            random_state=42,
            n_jobs=-1
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
            tol=1e-4
        )
        
        model = VotingRegressor([
            ('rf', rf_model),
            ('gb', gb_model)
        ], n_jobs=-1)

        cv_folds = min(10, max(3, len(df_clean) // 15))
        cv = KFold(n_splits=cv_folds, shuffle=True, random_state=42)
        
        scoring_metrics = ['r2', 'neg_mean_squared_error', 'neg_mean_absolute_error']
        cv_results = {}
        
        for metric in scoring_metrics:
            scores = cross_val_score(model, X, y, scoring=metric, cv=cv, n_jobs=-1)
            cv_results[metric] = {
                'mean': np.mean(scores),
                'std': np.std(scores)
            }
        
        mean_r2 = round(cv_results['r2']['mean'], 4)
        std_r2 = round(cv_results['r2']['std'], 4)

        model.fit(X, y)
        
        y_pred_train = model.predict(X)
        train_r2 = r2_score(y, y_pred_train)
        train_mae = mean_absolute_error(y, y_pred_train)
        train_rmse = np.sqrt(mean_squared_error(y, y_pred_train))
        model_info = {
            "cv_r2_mean": mean_r2,
            "cv_r2_std": std_r2,
            "train_r2": train_r2,
            "train_mae": train_mae,
            "train_rmse": train_rmse,
            "data_samples": len(df_clean),
            "feature_count": len(feature_columns),
            "cv_folds": cv_folds
        }

        joblib_path, pickle_path = save_model_and_preprocessors(
            model, le_os, le_display, feature_columns, model_info
        )

        return Response({
            "message": "Model başarıyla eğitildi ve kaydedildi",
            "model_paths": {
                "joblib": joblib_path,
                "pickle": pickle_path
            },
            "model_performance": {
                "cross_validation_r2": f"{mean_r2:.4f} ± {std_r2:.4f}",
                "training_r2": f"{train_r2:.4f}",
                "mae": f"{train_mae:.2f}",
                "rmse": f"{train_rmse:.2f}"
            },
            "data_info": {
                "original_samples": len(df),
                "cleaned_samples": len(df_clean),
                "features_used": len(feature_columns)
            }
        })

    except Exception as e:
        traceback.print_exc()
        return Response({"error": str(e)}, status=400)
