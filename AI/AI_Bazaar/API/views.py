from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from sklearn.neighbors import KNeighborsRegressor
import pandas as pd
import os
from django.conf import settings

@api_view(['GET'])
def hello_api(request):
    data = {
        "message": "Merhaba, AI_Bazaar API çalışıyor!",
    }
    return Response(data)

@api_view(['GET'])
def product_list(request):
    products = [
        {
            "id": 1,
            "name": "ChatGPT Clone",
            "description": "Yapay zeka sohbet botu",
            "price": 299.99,
            "category": "AI Tools"
        },
        {
            "id": 2,
            "name": "Image Generator",
            "description": "AI görsel üretici",
            "price": 199.99,
            "category": "AI Tools"
        },
        {
            "id": 3,
            "name": "Voice Assistant",
            "description": "Sesli asistan AI",
            "price": 399.99,
            "category": "AI Tools"
        }
    ]
    
    return Response({
        "status": "success",
        "count": len(products),
        "products": products
    })

@api_view(['GET'])
def product_detail(request, product_id):
    product = {
        "id": product_id,
        "name": f"AI Product {product_id}",
        "description": "Detaylı ürün açıklaması",
        "price": 299.99,
        "features": [
            "Advanced AI algorithms",
            "Real-time processing",
            "Easy integration"
        ],
        "rating": 4.5
    }
    
    return Response({
        "status": "success",
        "product": product
    })

@api_view(['POST'])
def create_product(request):
    data = request.data

    required_fields = ['name', 'description', 'price']
    for field in required_fields:
        if field not in data:
            return Response({
                "status": "error",
                "message": f"'{field}' alanı gerekli"
            }, status=status.HTTP_400_BAD_REQUEST)

    new_product = {
        "id": 999, 
        "name": data['name'],
        "description": data['description'],
        "price": data['price'],
        "created_at": "2024-01-01T00:00:00Z"
    }

    return Response({
        "status": "success",
        "message": "Ürün başarıyla oluşturuldu",
        "product": new_product
    }, status=status.HTTP_201_CREATED)


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

        df = pd.read_csv(
            r"C:\Users\pc\Desktop\AIbazaar\AIBazaar\AI\utils\csv\phones.csv"
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
        ]
        df = df[features + ["price_usd"]]

        # Ordinal encoding mapping'leri tanımla
        os_hierarchy = {
            "Android": 1,
            "iOS": 2,
            "HarmonyOS": 1.5,  # Android ve iOS arası
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
            "Micro LED": 8,
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

        # DataFrame'deki kategorik değişkenleri encode et
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

        # Yeni veri için encoding
        os_encoded = safe_map(os, os_hierarchy)
        display_type_encoded = safe_map(display_type, display_type_hierarchy)
        video_resolution_encoded = safe_map(
            video_resolution, video_resolution_hierarchy
        )

        # Yeni feature set oluştur (encoded değerlerle)
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
        ]

        x = df[feature_columns]
        y = df["price_usd"]

        # Yeni veri noktası
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
                }
            ]
        )

        # Feature scaling (opsiyonel ama KNN için önerilen)
        from sklearn.preprocessing import StandardScaler

        scaler = StandardScaler()
        x_scaled = scaler.fit_transform(x)
        new_data_scaled = scaler.transform(new_data)

        # Model eğitimi
        model = KNeighborsRegressor(
            n_neighbors=3, weights="distance"
        )  # distance weight'i daha iyi sonuç verebilir
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
