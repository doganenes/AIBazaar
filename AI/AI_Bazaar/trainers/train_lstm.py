import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, RobustScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.regularizers import L1L2
import holidays
from datetime import datetime
import tensorflow as tf
import random

def set_seeds(seed=42):
    tf.random.set_seed(seed)
    np.random.seed(seed)
    random.seed(seed)

class LSTMModelTrainer:
    def __init__(self, data_path,seed=42):
        self.data_path = data_path
        self.look_back = 7  
        self.forecast_horizon = 1  # Changed to 1 since we're predicting step-by-step
        self.seed = seed
        set_seeds(self.seed)

    def load_and_preprocess_data(self):
        """Load and clean the data"""
        df = pd.read_csv(self.data_path)
        
        # Convert and clean data
        df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
        df["RecordDate"] = pd.to_datetime(df["RecordDate"], errors="coerce")
        df["CurrencyRate"] = pd.to_numeric(df["CurrencyRate"], errors="coerce")
        df = df.dropna(subset=["RecordDate", "Price", "CurrencyRate"])
        
        df = df.sort_values("RecordDate")
        
        return df

    def create_features(self, product_df):
        set_seeds(self.seed)

        product_df['day_of_week'] = product_df['RecordDate'].dt.dayofweek
        product_df['day_of_month'] = product_df['RecordDate'].dt.day
        product_df['month'] = product_df['RecordDate'].dt.month
        
        tr_holidays = holidays.Turkey()
        product_df['is_holiday'] = product_df['RecordDate'].apply(lambda x: x in tr_holidays).astype(int)
        
        for lag in [1, 3, 7]:
            product_df[f'price_lag_{lag}'] = product_df['Price'].shift(lag)
            product_df[f'currency_lag_{lag}'] = product_df['CurrencyRate'].shift(lag)
        
        product_df['price_rolling_mean_7'] = product_df['Price'].rolling(window=7).mean()
        product_df['price_rolling_std_7'] = product_df['Price'].rolling(window=7).std()
        product_df['currency_rolling_mean_7'] = product_df['CurrencyRate'].rolling(window=7).mean()
        
        product_df = product_df.dropna()
        
        return product_df

    def prepare_sequences(self, features_scaled):
        """Prepare input-output sequences for LSTM"""
        X, y = [], []
        for i in range(len(features_scaled) - self.look_back):
            X.append(features_scaled[i:i + self.look_back])
            y.append(features_scaled[i + self.look_back, 0])  # Only predict next price
        return np.array(X), np.array(y)

    def create_model(self, input_shape):
        """Create LSTM model architecture"""
        model = Sequential([
            LSTM(128, input_shape=input_shape, return_sequences=True,
                 kernel_regularizer=L1L2(l1=1e-5, l2=1e-4)),
            Dropout(0.2),
            LSTM(64, return_sequences=False),
            Dropout(0.2),
            Dense(1)  # Single output for next price prediction
        ])
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        return model

    def train_and_predict(self, product_id, steps=15, min_data_points=30):
        """Main method to train and predict"""
        # Load and preprocess data
        set_seeds(self.seed)

        df = self.load_and_preprocess_data()
        product_df = df[df["ProductID"] == product_id].sort_values("RecordDate")
        
        if len(product_df) < min_data_points:
            raise ValueError(f"Not enough data for product {product_id}. Needs at least {min_data_points} records.")
        
        product_df = self.create_features(product_df)
        
        feature_cols = ['Price', 'CurrencyRate', 'day_of_week', 'is_holiday',
                       'price_lag_1', 'price_lag_3', 'currency_lag_1',
                       'price_rolling_mean_7', 'price_rolling_std_7']
        
        scalers = {}
        scaled_features = []
        for col in feature_cols:
            if col == 'Price':
                scaler = RobustScaler()
                scaled_col = scaler.fit_transform(product_df[[col]])
                scalers['price'] = scaler
            elif col == 'CurrencyRate':
                scaler = RobustScaler()
                scaled_col = scaler.fit_transform(product_df[[col]])
                scalers['currency'] = scaler
            else:
                scaler = MinMaxScaler()
                scaled_col = scaler.fit_transform(product_df[[col]])
                scalers[col] = scaler
            scaled_features.append(scaled_col)
        
        features_scaled = np.hstack(scaled_features)
        
        # Prepare sequences
        X, y = self.prepare_sequences(features_scaled)
        
        if len(X) == 0:
            raise ValueError(f"Not enough sequences for product {product_id}.")
        
        # Train model
        model = self.create_model(input_shape=(self.look_back, len(feature_cols)))
        model.fit(X, y, epochs=100, batch_size=16, verbose=0)
        
        # Evaluate model
        predictions = model.predict(X, verbose=0).flatten()
        y_inverse = scalers['price'].inverse_transform(y.reshape(-1, 1)).flatten()
        predictions_inverse = scalers['price'].inverse_transform(predictions.reshape(-1, 1)).flatten()
        
        # Calculate metrics
        mae = mean_absolute_error(y_inverse, predictions_inverse)
        mape = np.mean(np.abs((y_inverse - predictions_inverse) / 
                      np.maximum(np.abs(y_inverse), 1e-8))) * 100  # Avoid division by zero
        rmse = np.sqrt(mean_squared_error(y_inverse, predictions_inverse))
        r2 = r2_score(y_inverse, predictions_inverse)
        
        # Make future predictions
        last_sequence = features_scaled[-self.look_back:].reshape(1, self.look_back, len(feature_cols))
        future_predictions = []
        
        for _ in range(steps):
            # Predict next price
            pred_scaled = model.predict(last_sequence, verbose=0)[0][0]
            
            # Inverse transform the prediction
            dummy_input = np.zeros((1, len(feature_cols)))
            dummy_input[0, 0] = pred_scaled
            for i, col in enumerate(feature_cols[1:], 1):
                dummy_input[0, i] = last_sequence[0, -1, i] 
            
            pred_price = scalers['price'].inverse_transform(dummy_input[:, [0]])[0][0]
            future_predictions.append(pred_price)
            
            new_row = np.zeros((1, len(feature_cols)))
            new_row[0, 0] = pred_scaled
            new_row[0, 1:] = last_sequence[0, -1, 1:] 
            
            last_sequence = np.append(last_sequence[:, 1:, :], 
                                    new_row.reshape(1, 1, len(feature_cols)), 
                                    axis=1)
        
        return {
            "product": product_df["ProductName"].iloc[0],
            "productId": product_id,
            "steps": steps,
            "predicted_prices": [round(float(p), 2) for p in future_predictions],
            "metrics": {
                "mae": round(float(mae), 2),
                "mape": round(float(mape), 2),
                "rmse": round(float(rmse), 2),
                "r2": round(float(r2), 4)
            },
            "features_used": feature_cols
        }