import os
import pickle
import random
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, RobustScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout, Input
from tensorflow.keras.regularizers import L1L2
import holidays
from datetime import datetime
 
class LSTMMultiModelTrainer:
    def __init__(self, data_path, look_back=7, forecast_horizon=1, seed=42):
        self.data_path = data_path
        self.look_back = look_back
        self.forecast_horizon = forecast_horizon
        self.seed = seed
        self.set_seeds()
   
    def set_seeds(self):
        np.random.seed(self.seed)
        tf.random.set_seed(self.seed)
        random.seed(self.seed)
   
    def load_and_preprocess_data(self):
        # DtypeWarning için low_memory=False ekledik
        df = pd.read_csv(self.data_path, low_memory=False)
       
        # Sayısal dönüşümler
        df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
        df["CurrencyRate"] = pd.to_numeric(df["CurrencyRate"], errors="coerce")
       
        # Tarih dönüşümü
        df["RecordDate"] = pd.to_datetime(df["RecordDate"], errors="coerce")
       
        # NaN değerleri temizleme
        df = df.dropna(subset=["RecordDate", "Price", "CurrencyRate"])
       
        return df.sort_values("RecordDate")
   
    def create_features(self, product_df:pd.DataFrame):
        product_df = product_df.copy()
       
        # Tarih özellikleri (hiçbir veri kaybı yok)
        product_df['day_of_week'] = product_df['RecordDate'].dt.dayofweek
        product_df['day_of_month'] = product_df['RecordDate'].dt.day
        product_df['month'] = product_df['RecordDate'].dt.month
       
        # Tatil bilgisi (hiçbir veri kaybı yok)
        tr_holidays = holidays.Turkey()
        product_df['is_holiday'] = product_df['RecordDate'].apply(
            lambda x: x in tr_holidays).astype(int)
       
        # Gecikmeli özellikler - NaN'leri doldurma
        for lag in [1, 3, 7]:
            product_df[f'price_lag_{lag}'] = product_df['Price'].shift(lag).fillna(method='bfill')
            product_df[f'currency_lag_{lag}'] = product_df['CurrencyRate'].shift(lag).fillna(method='bfill')
       
        # Hareketli ortalamalar - min_periods ile NaN kontrolü
        product_df['price_rolling_mean_7'] = product_df['Price'].rolling(
            window=7, min_periods=1).mean()
        product_df['price_rolling_std_7'] = product_df['Price'].rolling(
            window=7, min_periods=1).std().fillna(0)  # std için 0 doldur
        product_df['currency_rolling_mean_7'] = product_df['CurrencyRate'].rolling(
            window=7, min_periods=1).mean()
       
        return product_df  
   
    def prepare_sequences(self, features_scaled):
        X, y = [], []
        for i in range(len(features_scaled) - self.look_back):
            X.append(features_scaled[i:i + self.look_back])
            y.append(features_scaled[i + self.look_back, 0])
        return np.array(X), np.array(y)
   
    def create_model(self, input_shape):
        model = Sequential([
            Input(shape=input_shape),  # Input layer eklendi
            LSTM(128, return_sequences=True,
                 kernel_regularizer=L1L2(l1=1e-5, l2=1e-4)),
            Dropout(0.2),
            LSTM(64, return_sequences=False),
            Dropout(0.2),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        return model
   
    def scale_features(self, product_df, feature_cols):
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
       
        return np.hstack(scaled_features), scalers
   
    def save_artifacts(self, model, scalers, product_id, save_dir="product_models"):
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
       
        model_path = os.path.join(save_dir, f"{product_id}_model.h5")
        model.save(model_path)
       
        scalers_path = os.path.join(save_dir, f"{product_id}_scalers.pkl")
        with open(scalers_path, 'wb') as f:
            pickle.dump(scalers, f)
       
        return model_path, scalers_path
   
    def train_for_all_products(self, min_data_points=30, epochs=100, batch_size=16):
        df = self.load_and_preprocess_data()
        product_ids = df['ProductID'].unique()
        results = {}
       
        feature_cols = ['Price', 'CurrencyRate', 'day_of_week', 'is_holiday',
                      'price_lag_1', 'price_lag_3', 'currency_lag_1',
                      'price_rolling_mean_7', 'price_rolling_std_7']
       
        for product_id in product_ids:
            try:
                self.set_seeds()
               
                product_df = df[df["ProductID"] == product_id].sort_values("RecordDate")
                if len(product_df) < min_data_points:
                    print(f"Ürün {product_id} için yeterli veri yok. Atlanıyor...")
                    continue
               
                product_df = self.create_features(product_df)
                features_scaled, scalers = self.scale_features(product_df, feature_cols)
               
                X, y = self.prepare_sequences(features_scaled)
                if len(X) == 0:
                    print(f"Ürün {product_id} için yeterli sequence yok. Atlanıyor...")
                    continue
               
                model = self.create_model(input_shape=(self.look_back, len(feature_cols)))
                history = model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=0)
               
                model_path, scalers_path = self.save_artifacts(model, scalers, product_id)
               
                results[product_id] = {
                    'product_name': product_df['ProductName'].iloc[0],
                    'model_path': model_path,
                    'scalers_path': scalers_path,
                    'train_samples': len(X),
                    'last_loss': history.history['loss'][-1],
                    'last_mae': history.history['mae'][-1]
                }
               
                print(f"Ürün {product_id} için model başarıyla eğitildi ve kaydedildi.")
               
            except Exception as e:
                print(f"Ürün {product_id} için hata oluştu: {str(e)}")
                continue
       
        return results
 
 
if __name__ == "__main__":
    # TensorFlow oneDNN uyarılarını devre dışı bırakma
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
   
    # Model eğiticiyi oluştur
    trainer = LSTMMultiModelTrainer(
        r"C:\Users\pc\Desktop\AIBazaar2\AIBazaar\AI\utils\notebooks\LSTMPriceHistory.csv"
    )
   
    # Tüm ürünler için model eğit
    training_results = trainer.train_for_all_products(
        min_data_points=30,
        epochs=100,
        batch_size=16
    )
    import json
    output_path = "egitim_sonuclari.json"
    # Sonuçları görüntüle
    print("\nEğitim Sonuçları:")
    for product_id, result in training_results.items():
        print(f"\nÜrün ID: {product_id}")
        print(f"Ürün Adı: {result['product_name']}")
        print(f"Eğitim Örnek Sayısı: {result['train_samples']}")
        print(f"Son Loss Değeri: {result['last_loss']:.4f}")
        print(f"Son MAE Değeri: {result['last_mae']:.4f}")
        print(f"Model Yolu: {result['model_path']}")
        print(f"Scaler Yolu: {result['scalers_path']}")
       
       
training_results = {str(k): v for k, v in training_results.items()}
 
# JSON'a kaydet
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(training_results, f, ensure_ascii=False, indent=4)