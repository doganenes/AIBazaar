import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import matplotlib.pyplot as plt

# Tarih ve fiyat verisi (örnek)
raw_data = pd.read_csv(
    "LSTMPriceHistory.csv", sep="\t", header=None, names=["RecordDate", "Price"]
)
# Veri işleme
lines = [line.strip() for line in raw_data.strip().split("\n")]
records = []
for line in lines:
    try:
        date_str, price_str = line.split("\t")
        date = datetime.strptime(date_str.strip(), "%d.%m.%Y")
        price = float(price_str.strip().replace(",", "."))
        records.append((date, price))
    except:
        pass

df = pd.DataFrame(records, columns=["RecordDate", "Price"])

# Eksik veriler yerine sabit fiyatlar ekle (örnekleme amacıyla)
while len(df) < 100:
    last_date = df.iloc[-1]["RecordDate"]
    next_date = last_date + pd.Timedelta(days=1)
    df = pd.concat(
        [
            df,
            pd.DataFrame(
                {
                    "RecordDate": [next_date],
                    "Price": [df["Price"].iloc[-1] + np.random.uniform(0, 5)],
                }
            ),
        ],
        ignore_index=True,
    )

# LSTM için veriyi hazırlama
scaler = MinMaxScaler()
scaled_prices = scaler.fit_transform(df[["Price"]])
sequence_length = 10

X, y = [], []
for i in range(len(scaled_prices) - sequence_length):
    X.append(scaled_prices[i : i + sequence_length])
    y.append(scaled_prices[i + sequence_length])
X, y = np.array(X), np.array(y)
X = X.reshape((X.shape[0], X.shape[1], 1))

# LSTM model tanımı
model = Sequential()
model.add(LSTM(50, activation="relu", input_shape=(sequence_length, 1)))
model.add(Dense(1))
model.compile(optimizer="adam", loss="mse")
model.fit(X, y, epochs=30, verbose=1)

# 15 gün ileriye tahmin
forecast = []
last_sequence = scaled_prices[-sequence_length:]
for _ in range(15):
    input_seq = last_sequence.reshape((1, sequence_length, 1))
    pred_scaled = model.predict(input_seq, verbose=0)[0][0]
    forecast.append(pred_scaled)
    last_sequence = np.append(last_sequence[1:], [[pred_scaled]], axis=0)

# Skaler ters dönüşüm (normalize → gerçek fiyat)
forecast_prices = scaler.inverse_transform(np.array(forecast).reshape(-1, 1)).flatten()

# Tahmini yazdır
for i, price in enumerate(forecast_prices, 1):
    print(f"Gün {i}: {price:.2f} TL")

# Grafik çiz
plt.plot(range(1, 16), forecast_prices, marker="o")
plt.title("15 Günlük LSTM Fiyat Tahmini")
plt.xlabel("Gün")
plt.ylabel("Tahmini Fiyat (TL)")
plt.grid(True)
plt.show()
