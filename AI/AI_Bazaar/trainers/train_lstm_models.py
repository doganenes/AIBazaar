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
        self.look_back = 5
        
        os.makedirs(model_dir, exist_ok=True)
    
    def load_data(self):
        df = pd.read_csv(self.data_path)
        df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
        df["RecordDate"] = pd.to_datetime(df["RecordDate"], errors="coerce")
        df = df.dropna(subset=["RecordDate", "Price"])
        return df
    
    def prepare_sequences(self, prices_scaled):
        """LSTM için sequence verilerini hazırla"""
        x, y = [], []
        for i in range(len(prices_scaled) - self.look_back):
            x.append(prices_scaled[i:i+self.look_back])
            y.append(prices_scaled[i+self.look_back])
        return np.array(x), np.array(y)
    
    def create_model(self):
        """LSTM modelini oluştur"""
        model = Sequential()
        model.add(LSTM(64, input_shape=(self.look_back, 1)))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        return model
    
    def train_product_model(self, product_name, product_df):
        """Belirli bir ürün için model eğit"""
        print(f"Training model for: {product_name}")
        
        prices = product_df["Price"].values.reshape(-1, 1)
        
        scaler = MinMaxScaler()
        prices_scaled = scaler.fit_transform(prices)
        
        x, y = self.prepare_sequences(prices_scaled)
        
        if len(x) == 0:
            print(f"Not enough data for {product_name}")
            return False
        
        model = self.create_model()
        model.fit(x, y, epochs=50, batch_size=4, verbose=1)
        
        model_path = os.path.join(self.model_dir, f"{product_name}_lstm_model.h5")
        scaler_path = os.path.join(self.model_dir, f"{product_name}_scaler.pkl")
        
        model.save(model_path)
        with open(scaler_path, 'wb') as f:
            pickle.dump(scaler, f)
        
        print(f"Model saved: {model_path}")
        print(f"Scaler saved: {scaler_path}")
        return True
    
    def train_all_products(self, min_data_points=20):
        df = self.load_data()
        
        products = df['ProductName'].unique()
        print(f"Found {len(products)} unique products")
        
        successful_trainings = 0
        failed_trainings = 0
        
        for product in products:
            product_df = df[df["ProductName"] == product].sort_values("RecordDate")
            
            if len(product_df) >= min_data_points:
                success = self.train_product_model(product, product_df)
                if success:
                    successful_trainings += 1
                else:
                    failed_trainings += 1
            else:
                print(f"Skipping {product}: Only {len(product_df)} data points (need {min_data_points})")
                failed_trainings += 1
        
        print(f"\nTraining Summary:")
        print(f"Successful: {successful_trainings}")
        print(f"Failed/Skipped: {failed_trainings}")
        
        return successful_trainings, failed_trainings
    
    def get_available_products(self):
        models = []
        for file in os.listdir(self.model_dir):
            if file.endswith('_lstm_model.h5'):
                product_name = file.replace('_lstm_model.h5', '')
                models.append(product_name)
        return models
    
    def predict_price(self, product_name, steps=1):
        model_path = os.path.join(self.model_dir, r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\models\general_lstm_model.h5")
        scaler_path = os.path.join(self.model_dir, r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\models\general_scaler.pkl")

        if not os.path.exists(model_path) or not os.path.exists(scaler_path):
            raise FileNotFoundError("General LSTM model or scaler not found.")

        model = load_model(model_path)
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)

        df = self.load_data()
        product_df = df[df["ProductName"] == product_name].sort_values("RecordDate")

        if len(product_df) < self.look_back:
            raise ValueError(f"Not enough data to make prediction for: {product_name}")

        prices = product_df["Price"].values.reshape(-1, 1)
        prices_scaled = scaler.transform(prices)
        last_sequence = prices_scaled[-self.look_back:].reshape(1, self.look_back, 1)

        predictions = []
        current_sequence = last_sequence

        for _ in range(steps):
            next_price_scaled = model.predict(current_sequence, verbose=0)[0][0]
            predictions.append(next_price_scaled)
            current_sequence = np.append(current_sequence[:, 1:, :], [[[next_price_scaled]]], axis=1)

        predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()

        return {
            "product": product_name,
            "steps": steps,
            "predicted_prices": [round(float(p), 2) for p in predictions]
        }



def main():
    DATA_PATH = r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\notebooks\LSTMPriceHistory.csv"
    MODEL_DIR = r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\models"
    
    trainer = LSTMModelTrainer(DATA_PATH, MODEL_DIR)
    
    print("Starting LSTM model training for all products...")
    successful, failed = trainer.train_all_products(min_data_points=20)
    
    available_models = trainer.get_available_products()
    print(f"\nAvailable trained models: {len(available_models)}")
    for model in available_models[:10]: 
        print(f"- {model}")
    
    if len(available_models) > 10:
        print(f"... and {len(available_models) - 10} more")

if __name__ == "__main__":
    main()