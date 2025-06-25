import os
import pickle
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dense, Dropout, InputLayer
from tensorflow.keras.models import Sequential
from tensorflow.keras.regularizers import L1L2

MODEL_PATH = r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\AI_Bazaar\trainers\product_models"
DATA_PATH = r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\notebooks\LSTMPriceHistory.csv"

class LSTMMultiModelTrainer:
    def __init__(self, look_back=7, forecast_horizon=1, seed=42):
        self.look_back = look_back
        self.forecast_horizon = forecast_horizon
        self.seed = seed
        tf.random.set_seed(seed)
        np.random.seed(seed)
        self.data = self._load_data()

    def _load_data(self):
        """Veri setini yükler ve ön işleme yapar"""
        df = pd.read_csv(DATA_PATH)
        df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
        df["CurrencyRate"] = pd.to_numeric(df["CurrencyRate"], errors="coerce")
        df["RecordDate"] = pd.to_datetime(df["RecordDate"], errors="coerce")
        return df.dropna(subset=["RecordDate", "Price", "CurrencyRate"])

    def _get_product_data(self, product_id):
        """Belirtilen product_id'ye ait son verileri getirir"""
        product_data = self.data[self.data["ProductID"] == product_id]
        if len(product_data) < self.look_back:
            raise ValueError(f"{product_id} için yeterli veri yok (en az {self.look_back} kayıt gerekli)")
        
        return product_data.sort_values("RecordDate").tail(self.look_back * 2)  # Buffer ile alıyoruz

    def _prepare_input_sequence(self, product_data):
        """Model için giriş dizisini hazırlar"""
        # Özellik mühendisliği
        product_data = product_data.copy()
        product_data['day_of_week'] = product_data['RecordDate'].dt.dayofweek
        product_data['day_of_month'] = product_data['RecordDate'].dt.day
        product_data['month'] = product_data['RecordDate'].dt.month
        product_data['is_holiday'] = 0  # Basitlik için
        
        # Gecikmeli özellikler
        for lag in [1, 3, 7]:
            product_data[f'price_lag_{lag}'] = product_data['Price'].shift(lag)
            product_data[f'currency_lag_{lag}'] = product_data['CurrencyRate'].shift(lag)
        
        # Hareketli ortalamalar
        product_data['price_rolling_mean_7'] = product_data['Price'].rolling(window=7).mean()
        product_data['price_rolling_std_7'] = product_data['Price'].rolling(window=7).std()
        product_data['currency_rolling_mean_7'] = product_data['CurrencyRate'].rolling(window=7).mean()
        
        # Son look_back kaydı al
        prepared_data = product_data.dropna().tail(self.look_back)
        
        # Özellik sırası
        feature_cols = ['Price', 'CurrencyRate', 'day_of_week', 'is_holiday',
                       'price_lag_1', 'price_lag_3', 'currency_lag_1',
                       'price_rolling_mean_7', 'price_rolling_std_7']
        
        return prepared_data[feature_cols].values

    def load_model(self, product_id, models_dir=MODEL_PATH):
        """Modeli ve scaler'ları yükler"""
        try:
            # Scaler'ları yükle
            scalers_path = os.path.join(models_dir, f"{product_id}_scalers.pkl")
            if not os.path.exists(scalers_path):
                raise FileNotFoundError(f"Scalers not found: {scalers_path}")
            
            with open(scalers_path, 'rb') as f:
                scalers = pickle.load(f)
            
            # Model yapısını oluştur
            model = Sequential([
                InputLayer(input_shape=(self.look_back, 9)),
                LSTM(128, return_sequences=True, 
                    kernel_regularizer=L1L2(l1=1e-5, l2=1e-4)),
                Dropout(0.2),
                LSTM(64, return_sequences=False),
                Dropout(0.2),
                Dense(1)
            ])
            
            # Ağırlıkları yükle
            weights_path = os.path.join(models_dir, f"{product_id}_model.h5")
            if not os.path.exists(weights_path):
                raise FileNotFoundError(f"Model weights not found: {weights_path}")
            
            model.load_weights(weights_path)
            model.compile(optimizer='adam')
            
            return model, scalers
            
        except Exception as e:
            raise RuntimeError(f"Model loading failed: {str(e)}")

    def predict_with_model(self, product_id, steps=15):
        """Tahmin yapmak için ana fonksiyon"""
        try:
            # 1. Model ve scaler'ları yükle
            model, scalers = self.load_model(product_id)
            
            # 2. Product verilerini getir
            product_data = self._get_product_data(product_id)
            
            # 3. Giriş dizisini hazırla ve ölçekle
            input_sequence = self._prepare_input_sequence(product_data)
            
            # Özellik sırası
            feature_cols = ['Price', 'CurrencyRate', 'day_of_week', 'is_holiday',
                          'price_lag_1', 'price_lag_3', 'currency_lag_1',
                          'price_rolling_mean_7', 'price_rolling_std_7']
            
            # Ölçekleme
            scaled_sequence = np.zeros_like(input_sequence)
            for i, col in enumerate(feature_cols):
                if col in scalers:
                    scaled_sequence[:, i] = scalers[col].transform(input_sequence[:, i].reshape(-1, 1)).flatten()
                else:
                    scaled_sequence[:, i] = input_sequence[:, i]
            
            # 4. Tahminleri yap
            predictions = []
            current_sequence = scaled_sequence.reshape(1, self.look_back, len(feature_cols))
            
            for _ in range(steps):
                # Tahmin yap
                pred_scaled = model(current_sequence, training=False).numpy()[0][0]
                
                # Ters ölçekleme
                dummy = np.zeros((1, len(feature_cols)))
                dummy[0, 0] = pred_scaled
                for i in range(1, len(feature_cols)):
                    dummy[0, i] = current_sequence[0, -1, i]
                
                pred_price = scalers['price'].inverse_transform(dummy[:, [0]])[0][0]
                predictions.append(float(round(pred_price, 2)))
                
                # Sequence güncelleme
                new_row = np.zeros((1, 1, len(feature_cols)))
                new_row[0, 0, 0] = pred_scaled
                new_row[0, 0, 1:] = current_sequence[0, -1, 1:]
                current_sequence = np.concatenate([current_sequence[:, 1:, :], new_row], axis=1)
            
            return {
                'product_id': product_id,
                'product_name': product_data['ProductName'].iloc[0],
                'last_actual_price': float(product_data['Price'].iloc[-1]),
                'predictions': predictions
            }
            
        except Exception as e:
            raise RuntimeError(f"Prediction failed for product {product_id}: {str(e)}")

# Kullanım örneği
if __name__ == "__main__":
    try:
        trainer = LSTMMultiModelTrainer()
        result = trainer.predict_with_model(682384, steps=10)
        print("Product Name:", result['product_name'])
        print("Last Actual Price:", result['last_actual_price'])
        print("Predictions:", result['predictions'])
    except Exception as e:
        print("Error:", str(e))