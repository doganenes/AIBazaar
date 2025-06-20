import os
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import load_model

class LSTMModelTrainer:
    def __init__(self, data_path, model_dir):
        self.data_path = data_path
        self.model_dir = model_dir
        self.look_back = 20
        
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
            x.append(prices_scaled[i:i+self.look_back])
            y.append(prices_scaled[i+self.look_back])
        return np.array(x), np.array(y)
    
    def create_model(self):
        model = Sequential()
        model.add(LSTM(64, input_shape=(self.look_back, 1)))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        return model

    def train_general_model(self, min_data_points=20):
        df = self.load_data()
        df = df.sort_values(by=["ProductID", "RecordDate"])

        # Yeterli veriye sahip ürünleri al
        valid_products = df.groupby("ProductID").filter(lambda x: len(x) >= min_data_points)

        if valid_products.empty:
            print("Yeterli veriye sahip ürün bulunamadı.")
            return False

        prices = valid_products["Price"].values.reshape(-1, 1)
        scaler = MinMaxScaler()
        prices_scaled = scaler.fit_transform(prices)
        x, y = self.prepare_sequences(prices_scaled)

        if len(x) == 0:
            print("Model eğitimi için yeterli sequence yok.")
            return False

        model = self.create_model()
        model.fit(x, y, epochs=50, batch_size=4, verbose=1)

        model_path = os.path.join(self.model_dir, "general_lstm_model.h5")
        scaler_path = os.path.join(self.model_dir, "general_scaler.pkl")

        model.save(model_path)
        with open(scaler_path, "wb") as f:
            pickle.dump(scaler, f)

        print(f"Model saved to: {model_path}")
        print(f"Scaler saved to: {scaler_path}")
        return True

    def predict_price(self, product_id, steps=1):
        model_path = os.path.join(self.model_dir, "general_lstm_model.h5")
        scaler_path = os.path.join(self.model_dir, "general_scaler.pkl")

        if not os.path.exists(model_path) or not os.path.exists(scaler_path):
            raise FileNotFoundError("Model or scaler not found.")

        model = load_model(model_path)
        with open(scaler_path, "rb") as f:
            scaler = pickle.load(f)

        df = self.load_data()
        product_df = df[df["ProductID"] == int(product_id)].sort_values("RecordDate")

        if product_df.empty:
            raise ValueError("Product not found.")
        if len(product_df) < self.look_back:
            raise ValueError("Not enough data for prediction.")

        prices = product_df["Price"].values.reshape(-1, 1)
        prices_scaled = scaler.transform(prices)
        last_sequence = prices_scaled[-self.look_back:].reshape(1, self.look_back, 1)

        predictions = []
        current_sequence = last_sequence

        for _ in range(steps):
            next_scaled = model.predict(current_sequence, verbose=0)[0][0]
            predictions.append(next_scaled)
            current_sequence = np.append(current_sequence[:, 1:, :], [[[next_scaled]]], axis=1)

        predicted_prices = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()
        product_name = product_df["ProductName"].iloc[0]

        return {
            "product": product_name,
            "productId": product_id,
            "steps": steps,
            "predicted_prices": [round(float(p), 2) for p in predicted_prices]
        }


def main():
    DATA_PATH = r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\notebooks\LSTMPriceHistory.csv"
    MODEL_DIR = r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\models"

    trainer = LSTMModelTrainer(DATA_PATH, MODEL_DIR)
    trainer.train_general_model(min_data_points=20)

if __name__ == "__main__":
    main()
