import os
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense 
 
class LSTMModelTrainer:
    def __init__(self, data_path, model_dir):
        self.data_path = data_path
        self.model_dir = model_dir
        self.look_back = 5
 
        os.makedirs(model_dir, exist_ok=True)
 
    def load_data(self):
        df = pd.read_csv(self.data_path)
        df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
        df["RecordDate"] = pd.to_datetime(df["RecordDate"], errors="coerce")
        df = df.dropna(subset=["RecordDate", "Price"])
        return df
 
    def prepare_sequences(self, prices_scaled):
        x, y = [], []
        for i in range(len(prices_scaled) - self.look_back):
            x.append(prices_scaled[i : i + self.look_back])
            y.append(prices_scaled[i + self.look_back])
        return np.array(x), np.array(y)
 
    def create_model(self):
        model = Sequential()
        model.add(LSTM(64, input_shape=(self.look_back, 1)))
        model.add(Dense(1))
        model.compile(loss="mean_squared_error", optimizer="adam")
        return model
 
    def train_general_model(self, min_data_points=100):
        df = self.load_data()
        df = df.sort_values("RecordDate")
        df = df.drop_duplicates(subset=["RecordDate", "ProductName"])
 
        prices = df["Price"].values.reshape(-1, 1)
 
        if len(prices) < min_data_points:
            print(
                f"Not enough total data: {len(prices)} rows (min required: {min_data_points})"
            )
            return False
 
        scaler = MinMaxScaler()
        prices_scaled = scaler.fit_transform(prices)
 
        x, y = self.prepare_sequences(prices_scaled)
 
        model = self.create_model()
        model.fit(x, y, epochs=50, batch_size=4, verbose=1)
 
        model_path = os.path.join(self.model_dir, "general_lstm_model.h5")
        scaler_path = os.path.join(self.model_dir, "general_scaler.pkl")
 
        model.save(model_path)
        with open(scaler_path, "wb") as f:
            pickle.dump(scaler, f)
 
        print(f"General model saved: {model_path}")
        print(f"General scaler saved: {scaler_path}")
        return True
 
    def get_available_model(self):
        return (
            "general_lstm_model.h5"
            if os.path.exists(os.path.join(self.model_dir, "general_lstm_model.h5"))
            else None
        )
 
 
def main():
    DATA_PATH = r"C:\\Users\\EXCALIBUR\\Desktop\\projects\\Okul Ödevler\\AIBazaar\\AI\\utils\\notebooks\\LSTMPriceHistory.csv"
    MODEL_DIR = r"C:\\Users\\EXCALIBUR\\Desktop\\projects\\Okul Ödevler\\AIBazaar\\AI\\utils\\models"
 
    trainer = LSTMModelTrainer(DATA_PATH, MODEL_DIR)
 
    print("Training general LSTM model on all product price history...")
    success = trainer.train_general_model(min_data_points=100)
 
    if success:
        print("✅ General model training completed successfully.")
    else:
        print("❌ General model training failed.")
 
 
if __name__ == "__main__":
    main()
 
 