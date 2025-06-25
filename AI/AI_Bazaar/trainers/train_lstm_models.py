import os
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense

class LSTMModelTrainer:
    def __init__(self, data_path, model_dir):
        self.data_path = data_path
        self.model_dir = model_dir
        self.look_back = 20

        self.current_model = None
        self.current_scaler = None
        self.current_product_id = None
        self.current_accuracy = None

        os.makedirs(model_dir, exist_ok=True)

    def load_data(self):
        df = pd.read_csv(self.data_path)
        df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
        df["RecordDate"] = pd.to_datetime(df["RecordDate"], errors="coerce")
        df["CurrencyRate"] = pd.to_numeric(df["CurrencyRate"], errors="coerce")
        df = df.dropna(subset=["RecordDate", "Price", "CurrencyRate"])
        return df

    def prepare_sequences(self, features_scaled):
        x, y = [], []
        for i in range(len(features_scaled) - self.look_back):
            x.append(features_scaled[i:i + self.look_back])
            y.append(features_scaled[i + self.look_back][0])
        return np.array(x), np.array(y)

    def create_model(self):
        model = Sequential()
        model.add(LSTM(64, input_shape=(self.look_back, 2)))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        return model

    def train_product_specific_model(self, product_id, min_data_points=20):
        df = self.load_data()
        product_df = df[df["ProductID"] == int(product_id)].sort_values("RecordDate")

        if product_df.empty or len(product_df) < min_data_points:
            return False, None

        # Ayrı ayrı scaler
        price_scaler = MinMaxScaler()
        rate_scaler = MinMaxScaler()

        scaled_price = price_scaler.fit_transform(product_df[["Price"]])
        scaled_rate = rate_scaler.fit_transform(product_df[["CurrencyRate"]])
        features_scaled = np.hstack((scaled_price, scaled_rate))

        x, y = self.prepare_sequences(features_scaled)
        if len(x) == 0:
            return False, None

        model = self.create_model()
        history = model.fit(
            x, y, epochs=50,
            batch_size=min(4, len(x)),
            validation_split=0.2 if len(x) >= 5 else 0,
            verbose=1
        )

        final_loss = history.history['loss'][-1]
        val_loss = history.history.get('val_loss', [final_loss])[-1]

        predictions = model.predict(x, verbose=0).flatten()
        print("Predictions" ,predictions)
        mae = mean_absolute_error(y, predictions)
        mape = np.mean(np.abs((y - predictions) / np.maximum(np.abs(y), 1e-8))) * 100
 
        rmse = 1 - np.sqrt(mean_squared_error(y, predictions))

        self.current_model = model
        self.current_scaler = {
            "price": price_scaler,
            "rate": rate_scaler
        }
        self.current_product_id = product_id
        self.current_accuracy = {
            'training_loss': round(final_loss, 6),
            'validation_loss': round(val_loss, 6),
            'lstm_accuracy': round(rmse, 6)
        }

        return True, self.current_accuracy

    def predict_price(self, product_id, steps=1):
        if (self.current_model is not None and
            self.current_scaler is not None and
            str(self.current_product_id) == str(product_id)):
            model = self.current_model
            scalers = self.current_scaler
        else:
            model = load_model(os.path.join(self.model_dir, "general_lstm_model.h5"))
            with open(os.path.join(self.model_dir, "general_scaler.pkl"), "rb") as f:
                scalers = pickle.load(f)

        df = self.load_data()
        product_df = df[df["ProductID"] == int(product_id)].sort_values("RecordDate")

        if product_df.empty or len(product_df) < self.look_back:
            raise ValueError("Yetersiz veri.")

        price_scaler = scalers["price"]
        rate_scaler = scalers["rate"]

        scaled_price = price_scaler.transform(product_df[["Price"]])
        scaled_rate = rate_scaler.transform(product_df[["CurrencyRate"]])
        features_scaled = np.hstack((scaled_price, scaled_rate))

        last_sequence = features_scaled[-self.look_back:].reshape(1, self.look_back, 2)

        predictions = []
        current_sequence = last_sequence

        for _ in range(steps):
            next_scaled_price = model.predict(current_sequence, verbose=0)[0][0]
            predictions.append(next_scaled_price)
            last_currency_rate = current_sequence[0, -1, 1]
            next_step = np.array([[next_scaled_price, last_currency_rate]])
            current_sequence = np.append(current_sequence[:, 1:, :], next_step.reshape(1, 1, 2), axis=1)

        inverse_input = np.array([[p] for p in predictions])
        predicted_prices = price_scaler.inverse_transform(inverse_input).flatten()

        return {
            "product": product_df["ProductName"].iloc[0],
            "productId": product_id,
            "steps": steps,
            "predicted_prices": [round(float(p), 2) for p in predicted_prices],
        }