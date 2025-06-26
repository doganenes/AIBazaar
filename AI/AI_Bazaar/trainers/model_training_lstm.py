import pickle

import numpy as np
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import MinMaxScaler, RobustScaler
from train_lstm import LSTMModelTrainer  # Assuming your class is in this file
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

class GeneralLSTMModel:
    def __init__(self, data_path, seed=42):
        self.data_path = data_path
        self.trainer = LSTMModelTrainer(data_path, seed)
        self.model = None
        self.scalers = None
        self.feature_cols = None
        self.look_back = None
 
    def load_and_preprocess_data(self):
        df = pd.read_csv(
            self.data_path,
            dtype={'Price': str},
            parse_dates=['RecordDate'],
            dayfirst=True,
            low_memory=False
        )
        
        # Clean and convert Price
        df["Price"] = (
            df["Price"]
            .str.replace('.', '', regex=False)
            .str.replace(',', '.', regex=False)
            .apply(pd.to_numeric, errors='coerce')
        )
        
        # Add price validation
        def validate_price(price):
            if pd.isna(price):
                return False
            # Set reasonable min/max price bounds
            return 1000 <= price <= 500000  # Adjust these values based on your domain knowledge
        
        # Filter out invalid prices
        valid_prices = df['Price'].apply(validate_price)
        df = df[valid_prices]
        
        # Clean CurrencyRate
        df["CurrencyRate"] = (
            df["CurrencyRate"]
            .astype(str)
            .str.replace(',', '.', regex=False)
            .apply(pd.to_numeric, errors='coerce')
        )
        
        df = df.dropna(subset=["Price", "CurrencyRate"])
        return df

    def train_general_model(self, min_data_points=20):
        """Train a general model on all available products"""
        df = self.load_and_preprocess_data()
        
        # Debug: Check data quality
        print(f"\nData Quality Report:")
        print(f"Total products: {len(df['ProductID'].unique())}")
        print(f"Total records: {len(df)}")
        print(f"Missing Prices: {df['Price'].isnull().sum()}")
        print(f"Zero Prices: {len(df[df['Price'] == 0])}")
        print(f"Negative Prices: {len(df[df['Price'] < 0])}\n")
        
        product_ids = df["ProductID"].unique()
        
        # Initialize variables to store combined data
        all_X = []
        all_y = []
        
        # Process each product and combine the sequences
        for product_id in product_ids:
            try:
                product_df = df[df["ProductID"] == product_id].sort_values("RecordDate")
                
                # Skip if not enough data
                if len(product_df) < min_data_points:
                    print(f"Skipping product {product_id}: insufficient data points ({len(product_df)} < {min_data_points})")
                    continue
                
                product_df = self.trainer.create_features(product_df)
                
                self.feature_cols = ['Price', 'CurrencyRate', 'day_of_week', 'is_holiday',
                                'price_lag_1', 'price_lag_3', 'currency_lag_1',
                                'price_rolling_mean_7', 'price_rolling_std_7']
                
                # Initialize scalers if not already done
                if self.scalers is None:
                    self.scalers = {}
                    scaled_features = []
                    for col in self.feature_cols:
                        try:
                            if col == 'Price':
                                # Use QuantileTransformer for prices to handle outliers
                                from sklearn.preprocessing import QuantileTransformer
                                scaler = QuantileTransformer(output_distribution='normal')
                                scaled_col = scaler.fit_transform(product_df[[col]].values.reshape(-1, 1))
                                self.scalers['price'] = scaler
                            # ... rest of scaler initialization ...
                        except Exception as e:
                            print(f"Error scaling column {col}: {str(e)}")
                            print(f"Values: {product_df[col].describe()}")
                            raise
                else:
                    # Use existing scalers to transform new data
                    scaled_features = []
                    for col in self.feature_cols:
                        try:
                            scaled_col = self.scalers[col].transform(product_df[[col]].values.reshape(-1, 1))
                            scaled_features.append(scaled_col)
                        except Exception as e:
                            print(f"Error transforming column {col} for product {product_id}: {str(e)}")
                            print(f"Problematic values: {product_df[col].unique()}")
                            raise
                
                features_scaled = np.hstack(scaled_features)
                
                # Prepare sequences
                X, y = self.trainer.prepare_sequences(features_scaled)
                
                if len(X) > 0:
                    all_X.append(X)
                    all_y.append(y)
                    
            except Exception as e:
                print(f"Error processing product {product_id}: {str(e)}")
                continue
        
        # Rest of your training code...
    def save_model(self, filepath):
        """Save the trained model and scalers to a pickle file"""
        if not self.model or not self.scalers:
            raise ValueError("Model and scalers must be trained before saving.")
        
        save_data = {
            'model': self.model,
            'scalers': self.scalers,
            'feature_cols': self.feature_cols,
            'look_back': self.look_back
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(save_data, f)
        
        print(f"Model saved to {filepath}")

# Example usage:
if __name__ == "__main__":
    data_path = r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\notebooks\LSTMPriceHistory.csv"  # Replace with your data path
    model_save_path = "general_lstm_model.pkl"
    
    # Create and train the general model
    general_model = GeneralLSTMModel(data_path)
    general_model.train_general_model()
    
    # Save the trained model
    general_model.save_model(model_save_path)