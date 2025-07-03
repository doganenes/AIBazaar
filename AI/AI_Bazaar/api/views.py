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

import warnings
from datetime import datetime
warnings.filterwarnings("ignore")
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.services.lstm_service import LSTMPredictor
from api.services.rf_service import PhonePricePredictor

@api_view(["POST"])
def predict_phone_price(request):
    try:

        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(base_dir)
        default_model_path = os.path.join(
            parent_dir, "models", "phone_price_model_20250630_225022.pkl"
        )

        model_path = request.data.get("model_path", default_model_path)

        input_data = {
            "ram": float(request.data.get("RAM")),
            "storage": float(request.data.get("Storage")),
            "display_size": float(request.data.get("Display Size")),
            "battery": float(request.data.get("Battery Capacity")),
            "ppi_density": int(request.data.get("Pixel Density")),
            "os_type": request.data.get("Operating System").strip().title(),
            "display_type": request.data.get("Display Technology").split(",")[0].strip().title(),
            "camera": float(request.data.get("camera")),
            "chipset": int(request.data.get("CPU Manufacturing")),
            "5g": int(request.data.get("5G")),
            "refresh_rate": int(request.data.get("Refresh Rate", 60)),
            "waterproof": int(request.data.get("Waterproof", 0)),
            "dustproof": int(request.data.get("Dustproof", 0)),
        }

        predictor = PhonePricePredictor(model_path=model_path)
        result = predictor.predict(input_data)

        return Response(result, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": str(e), "trace": traceback.format_exc()},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def predict_with_lstm_model(request):
    try:
        data = request.data
        product_id = int(data.get("product_id"))
        current_dir = os.path.dirname(os.path.abspath(__file__))

        parent_dir = os.path.dirname(current_dir)

        model_dir = os.path.join(parent_dir, "trainers", "product_models")


        if not product_id:
            return Response({"error": "product_id parametresi zorunludur"}, status=400)

        model_path = os.path.join(model_dir, f"{product_id}_model.h5")
        scalers_path = os.path.join(model_dir, f"{product_id}_scalers.pkl")

        if not os.path.exists(model_path):
            return Response({"error": f"Product {product_id} not found!"}, status=404)
        if not os.path.exists(scalers_path):
            return Response({"error": f"Product {product_id} for scaler not found!"}, status=404)

        predictor = LSTMPredictor(model_path, scalers_path)
        if not predictor.load_model_and_scalers():
            return Response({"error": "Model or scaler not load!"}, status=500)

        current_dir = os.path.dirname(os.path.abspath(__file__))  
        ai_bazaar_dir = os.path.dirname(current_dir)             
        ai_dir = os.path.dirname(ai_bazaar_dir)                   

        data_path = os.path.join(ai_dir, "utils", "notebooks", "LSTMPriceHistory.csv")
        if not os.path.exists(data_path):
            return Response({"error": "data path not found!"}, status=404)

        df = pd.read_csv(data_path, low_memory=False)
        df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
        df["CurrencyRate"] = pd.to_numeric(df["CurrencyRate"], errors="coerce")
        df["RecordDate"] = pd.to_datetime(df["RecordDate"], errors="coerce")
        df = df.dropna(subset=["RecordDate", "Price", "CurrencyRate"])

        product_df = df[df["ProductID"] == product_id].sort_values("RecordDate")
        if product_df.empty:
            return Response({"error": f"Product {product_id} for data not found!"}, status=404)

        if len(product_df) < predictor.look_back:
            return Response({
                "error": f"En az {predictor.look_back} günlük data gerekli, mevcut: {len(product_df)}"
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
                "r2": round(r2, 4) if r2 is not None else None  
            },
            "features_used": feature_cols
        })

    except Exception as e:
        traceback.print_exc()
        return Response({
            "error": f"An error occurred while estimation: {str(e)}",
            "success": False
        }, status=500)
