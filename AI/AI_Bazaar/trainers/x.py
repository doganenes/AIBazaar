import os
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dense, Dropout, InputLayer
from tensorflow.keras.models import Sequential
from tensorflow.keras.regularizers import L1L2

MODEL_PATH = r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\AI_Bazaar\trainers\product_models"


class LSTMMultiModelTrainer:
    def __init__(self, look_back=7, forecast_horizon=1, seed=42):
        self.look_back = look_back
        self.forecast_horizon = forecast_horizon
        self.seed = seed
        tf.random.set_seed(seed)
        np.random.seed(seed)
    
    def _load_model_weights(self, model, product_id, models_dir=MODEL_PATH):
        """Model ağırlıklarını saf TensorFlow ops ile yükler"""
        weights_path = os.path.join(models_dir, f"{product_id}_model.weights.h5")
        if not os.path.exists(weights_path):
            raise FileNotFoundError(f"Model weights not found: {weights_path}")
        
        # Model yapısını oluştur
        model.build(input_shape=(None, self.look_back, 9))  # 9 özellik olduğunu varsayalım
        
        # Ağırlıkları yükle
        model.load_weights(weights_path)
        return model

    def load_model(self, product_id, models_dir=MODEL_PATH):
        """Modeli ve scaler'ları TensorFlow saf API'si ile yükler"""
        try:
            # 1. Scaler'ları yükle
            scalers_path = os.path.join(models_dir, f"{product_id}_scalers.pkl")
            if not os.path.exists(scalers_path):
                raise FileNotFoundError(f"Scalers not found: {scalers_path}")
            
            with open(scalers_path, 'rb') as f:
                scalers = pickle.load(f)
            
            # 2. Model yapısını oluştur (orijinal yapıyla aynı)
            model = Sequential([
                InputLayer(input_shape=(self.look_back, 9)),
                LSTM(128, return_sequences=True, 
                    kernel_regularizer=L1L2(l1=1e-5, l2=1e-4)),
                Dropout(0.2),
                LSTM(64, return_sequences=False),
                Dropout(0.2),
                Dense(1)
            ])
            
            # 3. Ağırlıkları yükle
            model = self._load_model_weights(model, product_id, models_dir)
            
            # Modeli compile et (eğitim yapmayacağımız için loss fonksiyonu gerekmez)
            model.compile(optimizer='adam')
            
            return model, scalers
            
        except Exception as e:
            raise RuntimeError(f"Model loading failed: {str(e)}")

    def predict_with_model(self, product_id, steps=15, models_dir=MODEL_PATH):
        """Tahmin yapmak için optimizasyon"""
        try:
            model, scalers = self.load_model(product_id, models_dir)
            
            # Özellik sırası
            feature_cols = ['Price', 'CurrencyRate', 'day_of_week', 'is_holiday',
                          'price_lag_1', 'price_lag_3', 'currency_lag_1',
                          'price_rolling_mean_7', 'price_rolling_std_7']
            
            # Başlangıç sequence (gerçek uygulamada veritabanından alınmalı)
            last_sequence = np.zeros((1, self.look_back, len(feature_cols)))
            
            predictions = []
            for _ in range(steps):
                # TF fonksiyonu ile tahmin
                pred_scaled = model(last_sequence, training=False).numpy()[0][0]
                
                # Scaler ile ters dönüşüm
                dummy = np.zeros((1, len(feature_cols)))
                dummy[0, 0] = pred_scaled
                for i in range(1, len(feature_cols)):
                    dummy[0, i] = last_sequence[0, -1, i]
                
                pred_price = scalers['price'].inverse_transform(dummy[:, [0]])[0][0]
                predictions.append(float(round(pred_price, 2)))
                
                # Sequence güncelleme
                new_row = np.zeros((1, 1, len(feature_cols)))
                new_row[0, 0, 0] = pred_scaled
                new_row[0, 0, 1:] = last_sequence[0, -1, 1:]
                last_sequence = np.concatenate([last_sequence[:, 1:, :], new_row], axis=1)
            
            return predictions
            
        except Exception as e:
            raise RuntimeError(f"Prediction failed: {str(e)}")

# Kullanım örneği
if __name__ == "__main__":
    try:
        trainer = LSTMMultiModelTrainer()
        preds = trainer.predict_with_model("682384", steps=10)
        print("Predictions:", preds)
    except Exception as e:
        print("Error:", str(e))