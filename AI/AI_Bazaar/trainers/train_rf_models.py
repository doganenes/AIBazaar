import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Veri yükleme ve ön işleme fonksiyonları (aynısını kullanıyoruz)
def advanced_feature_engineering(df):
    """Gelişmiş özellik mühendisliği ile R2 skorunu artırma"""
    # ... (yukarıdaki advanced_feature_engineering fonksiyonunun aynısı)
    return df

def prepare_data(df):
    # Sütun adlarını yeniden adlandırma
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

    # Numerik dönüşüm
    numeric_columns = ["ram", "storage", "display_size", "battery", "ppi_density", 
                      "camera", "chipset", "5g", "refresh_rate", "waterproof", "dustproof", "price"]
    
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # NaN değerleri temizleme
    df = df.dropna(subset=numeric_columns)
    
    return df

def train_and_save_model():
    # Veri yükleme
    df = pd.read_csv(r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\notebooks\Product.csv")
    df = prepare_data(df)
    
    # 1. ÖNEMLİ DÜZELTME: advanced_feature_engineering'i prepare_data'dan SONRA çağır
    df = advanced_feature_engineering(df)
    
    # 2. ÖNEMLİ KONTROL: Tüm feature'ların oluştuğunu doğrula
    required_features = [
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
    
    # Eksik feature'ları kontrol et
    missing_features = [f for f in required_features if f not in df.columns]
    if missing_features:
        raise ValueError(f"Eksik özellikler: {missing_features}. advanced_feature_engineering fonksiyonunu kontrol edin.")
    
    # 3. OS ve display encoding
    le_os = LabelEncoder()
    df["os_encoded"] = le_os.fit_transform(df["os_type"])
    le_display = LabelEncoder()
    df["display_encoded"] = le_display.fit_transform(df["display_type"])
    
    feature_columns = required_features + ["os_encoded", "display_encoded"]
    
    # 4. X ve y'yi oluşturmadan önce son kontrol
    X = df[feature_columns].copy()
    y = df["price"]
    
    # ... (model eğitim ve kaydetme kısmı aynı)
if __name__ == "__main__":
    train_and_save_model()