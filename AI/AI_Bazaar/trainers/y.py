import pickle
import holidays
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
import traceback

import os
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, RobustScaler
import tensorflow as tf
from tensorflow.keras.models import load_model
import holidays
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
import traceback
class LSTMPredictor:
    def __init__(self, model_path, scalers_path):
        self.model_path = model_path
        self.scalers_path = scalers_path
        self.model = None
        self.scalers = None
        self.look_back = 7
        
    def load_model_and_scalers(self):
        """Kaydedilmiş LSTM modelini ve scaler'ları yükle"""
        try:
            # Model yükleme
            self.model = load_model(self.model_path,compile=False)
            
            # Scaler'ları yükleme
            with open(self.scalers_path, 'rb') as f:
                self.scalers = pickle.load(f)
                
            return True
        except Exception as e:
            print(f"Model yükleme hatası: {str(e)}")
            return False
    
    def create_features_for_prediction(self, product_df):
        """Tahmin için özellik mühendisliği"""
        product_df = product_df.copy()
        
        # Tarih özellikleri
        product_df['day_of_week'] = product_df['RecordDate'].dt.dayofweek
        product_df['day_of_month'] = product_df['RecordDate'].dt.day
        product_df['month'] = product_df['RecordDate'].dt.month
        
        # Tatil bilgisi
        tr_holidays = holidays.Turkey()
        product_df['is_holiday'] = product_df['RecordDate'].apply(
            lambda x: x in tr_holidays).astype(int)
        
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
    
    def scale_features_for_prediction(self, product_df, feature_cols):
        """Önceden eğitilmiş scaler'ları kullanarak özellikleri ölçeklendir"""
        scaled_features = []
        
        for col in feature_cols:
            if col == 'Price':
                scaler = self.scalers['price']
                scaled_col = scaler.transform(product_df[[col]])
            elif col == 'CurrencyRate':
                scaler = self.scalers['currency']
                scaled_col = scaler.transform(product_df[[col]])
            else:
                scaler = self.scalers[col]
                scaled_col = scaler.transform(product_df[[col]])
            scaled_features.append(scaled_col)
        
        return np.hstack(scaled_features)
    
    def prepare_sequence_for_prediction(self, features_scaled):
        """Son look_back kadar veriyi alarak tahmin için sequence hazırla"""
        if len(features_scaled) < self.look_back:
            raise ValueError(f"En az {self.look_back} günlük veri gerekli")
        
        # Son look_back kadar veriyi al
        sequence = features_scaled[-self.look_back:]
        return np.array([sequence])  # Batch dimension ekle
    
    def predict_next_15_days(self, sequence_scaled):
        """
        Ölçeklenmiş sequence ile 15 günlük fiyat tahmini yapar.
        Her tahmin çıktısı bir sonraki giriş dizisine eklenerek ilerlenir (recursive).
        """
        predictions_scaled = []
        current_sequence = sequence_scaled.copy()

        for _ in range(15):
            next_pred_scaled = self.model.predict(current_sequence, verbose=0)
            predictions_scaled.append(next_pred_scaled[0, 0])

            # Yeni tahmini mevcut sequence'e ekle, en eskiyi çıkar
            next_step = np.append(current_sequence[0, 1:, :], [[next_pred_scaled[0, 0]] + [0] * (current_sequence.shape[2] - 1)], axis=0)
            current_sequence = np.expand_dims(next_step, axis=0)

        # Ölçeklenmiş tahminleri orijinale çevir
        price_scaler = self.scalers['price']
        predictions_original = price_scaler.inverse_transform(np.array(predictions_scaled).reshape(-1, 1))

        return predictions_original.flatten().tolist()
