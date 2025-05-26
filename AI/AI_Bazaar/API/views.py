import base64
import io
from matplotlib import pyplot as plt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from sklearn.neighbors import KNeighborsRegressor
import pandas as pd
import os
from django.conf import settings
from statsmodels.tsa.arima.model import ARIMA

@api_view(["POST"])
def predict_product_knn(request):
    data = request.data

    try:
        ram = float(data.get("ram"))
        storage = float(data.get("storage"))
        display_size = float(data.get("display_size"))
        battery = float(data.get("battery"))
        foldable = int(data.get("foldable"))
        ppi = int(data.get("ppi"))
        os = data.get("os")
        display_type = data.get("display_type")
        video_resolution = data.get("video_resolution")
        chipset = int(data.get("chipset"))
        df = pd.read_csv(
            r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\csv\phones.csv"
        )

        features = [
            "ram",
            "storage",
            "display_size",
            "battery",
            "foldable",
            "ppi_density",
            "os",
            "display_type",
            "video_resolution",
            "chipset",
        ]
        df = df[features + ["price_usd"]]

        os_hierarchy = {
            "Android": 1,
            "iOS": 2,
            "HarmonyOS": 1.5,  
            "Windows": 0.5,
            "Other": 0,
        }

        display_type_hierarchy = {
            "LCD": 1,
            "IPS LCD": 2,
            "OLED": 3,
            "AMOLED": 4,
            "Super AMOLED": 5,
            "Dynamic AMOLED": 6,
            "LTPO OLED": 7,
            "Other": 0,
        }

        video_resolution_hierarchy = {
            "480p": 1,
            "720p": 2,
            "HD": 2,
            "1080p": 3,
            "Full HD": 3,
            "1440p": 4,
            "QHD": 4,
            "2K": 4,
            "4K": 5,
            "UHD": 5,
            "8K": 6,
            "Other": 0,
        }

        def safe_map(value, mapping, default=0):
            """Güvenli mapping fonksiyonu - eğer değer mapping'de yoksa default değer döner"""
            return mapping.get(value, default)

        df["os_encoded"] = df["os"].apply(lambda x: safe_map(x, os_hierarchy))
        df["display_type_encoded"] = df["display_type"].apply(
            lambda x: safe_map(x, display_type_hierarchy)
        )
        df["video_resolution_encoded"] = df["video_resolution"].apply(
            lambda x: safe_map(x, video_resolution_hierarchy)
        )

        df["chipset"] = df["chipset"].apply(
            lambda x: int(
                ''.join(filter(str.isdigit, x.split("(")[-1].split("nm")[0]))
            ) if isinstance(x, str) and "(" in x and "nm" in x else 0
        )

        os_encoded = safe_map(os, os_hierarchy)
        display_type_encoded = safe_map(display_type, display_type_hierarchy)
        video_resolution_encoded = safe_map(
            video_resolution, video_resolution_hierarchy
        )

        feature_columns = [
            "ram",
            "storage",
            "display_size",
            "battery",
            "foldable",
            "ppi_density",
            "os_encoded",
            "display_type_encoded",
            "video_resolution_encoded",
            "chipset",
        ]

        x = df[feature_columns]
        y = df["price_usd"]

        new_data = pd.DataFrame(
            [
                {
                    "ram": ram,
                    "storage": storage,
                    "display_size": display_size,
                    "battery": battery,
                    "foldable": foldable,
                    "ppi_density": ppi,
                    "os_encoded": os_encoded,
                    "display_type_encoded": display_type_encoded,
                    "video_resolution_encoded": video_resolution_encoded,
                    "chipset": chipset
                }
            ]
        )

        from sklearn.preprocessing import StandardScaler

        scaler = StandardScaler()
        x_scaled = scaler.fit_transform(x)
        new_data_scaled = scaler.transform(new_data)

        model = KNeighborsRegressor(
            n_neighbors=3, weights="distance"
        )  
        model.fit(x_scaled, y)

        prediction_price = model.predict(new_data_scaled)[0]

        print(f"Predicted price: {round(prediction_price, 2)}")
        print(
            f"Input encodings - OS: {os_encoded}, Display: {display_type_encoded}, Resolution: {video_resolution_encoded}"
        )

        return Response(
            {
                "message": "KNN prediction successful",
                "price": round(prediction_price, 2),
                "encodings": {
                    "os": os_encoded,
                    "display_type": display_type_encoded,
                    "video_resolution": video_resolution_encoded,
                },
            }
        )

    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        return Response({"error": str(e)}, status=400)



@api_view(['POST'])
def predict_product_arima(request):
    product_name = request.data.get('product')


    if not product_name:
        return Response({"error": "Lütfen 'product' alanını POST verisinde gönderin."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        df = pd.read_csv(r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\csv\akakce.csv")

        df["Price"] = df["Price"].apply(lambda x: int(str(x).replace(" TL", "").split(",")[0].replace(".", "")))
        df["Price"] = df["Price"].astype(int)

        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])

        product_df = df[df["Product Name"] == product_name].sort_values("Date")
        print(len(product_df))
        if len(product_df) < 1:
            return Response({"error": f"Yetersiz veri: {product_name}"}, status=status.HTTP_400_BAD_REQUEST)

        model = ARIMA(product_df["Price"], order=(2, 1, 1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=5).tolist()

        future_dates = pd.date_range(start=product_df["Date"].iloc[-1], periods=6, freq="D")[1:]

        return Response({
            "product": product_name,
            "forecast": forecast,
        })

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)