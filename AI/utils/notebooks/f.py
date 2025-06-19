import pandas as pd
import numpy as np

np.random.seed(42)

n_android = 150
n_ios = 20
n_total = n_android + n_ios

# Özellik seçenekleri
ram_options = [4, 6, 8, 12, 16]
storage_options = [64, 128, 256, 512]

# Android telefonlar için özellik seçimi
ram_android = np.random.choice(ram_options, n_android)
storage_android = np.random.choice(storage_options, n_android)

# iOS telefonlar için özellik seçimi
# iPhone'larda genelde daha yüksek ram ve storage tercih edilir diye biraz yükseklerden seçelim
ram_ios = np.random.choice([6, 8, 12, 16], n_ios)
storage_ios = np.random.choice([128, 256, 512], n_ios)

# OS tipi kolonları
os_android = ["Android"] * n_android
os_ios = ["iOS"] * n_ios

# Price: basit model, özelliklere göre, iOS için ekstra prim
base_price_android = 3000
base_price_ios = 9000  # iOS'lar Android'den genelde yüksek fiyatlı

# Android fiyat hesaplama
price_android = (
    base_price_android
    + ram_android * 1200
    + storage_android * 15
    + np.random.normal(0, 500, n_android)  # gürültü
)

# iOS fiyat hesaplama (özelliklere ek prim)
price_ios = (
    base_price_ios + ram_ios * 1300 + storage_ios * 20 + np.random.normal(0, 700, n_ios)
)

# Veri setini birleştir
df = pd.DataFrame(
    {
        "ram": np.concatenate([ram_android, ram_ios]),
        "storage": np.concatenate([storage_android, storage_ios]),
        "os_type": os_android + os_ios,
        "price": np.concatenate([price_android, price_ios]),
    }
)

# Gruplandırma (senin istediğin gibi)
df["ram_group"] = pd.cut(
    df["ram"], bins=[0, 4, 8, 12, 20], labels=["0-4", "5-8", "9-12", "13+"]
)
df["storage_group"] = pd.cut(
    df["storage"],
    bins=[0, 64, 128, 256, 512],
    labels=["0-64", "65-128", "129-256", "257+"],
)

# Örnek segment seçimi: 5-8 GB RAM ve 129-256 GB storage
group = df[(df["ram_group"] == "5-8") & (df["storage_group"] == "129-256")]

# OS bazında ortalama fiyatlar
mean_prices = group.groupby("os_type")["price"].mean()
print("Segment bazında OS fiyat ortalamaları:\n", mean_prices)
