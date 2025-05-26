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


@api_view(['POST'])
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

        df = pd.read_csv(r"C:\Users\EXCALIBUR\Desktop\projects\Okul Ödevler\AIBazaar\AI\utils\csv\phones.csv")

        features = ["ram", "storage", "display_size", "battery", "foldable", "ppi_density", "os", "display_type", "video_resolution"]
        df = df[features + ["price_usd"]]

        df = pd.get_dummies(df, columns=["os", "display_type", "video_resolution"])

        new_data = pd.DataFrame([{
            "ram": ram,
            "storage": storage,
            "display_size": display_size,
            "battery": battery,
            "foldable": foldable,
            "ppi_density": ppi,
            "os": os,
            "display_type": display_type,
            "video_resolution": video_resolution
        }])

        new_data = pd.get_dummies(new_data)

        missing_cols = [col for col in df.columns if col not in new_data.columns and col != "price_usd"]
        zeros_df = pd.DataFrame(0, index=new_data.index, columns=missing_cols)
        new_data = pd.concat([new_data, zeros_df], axis=1)

        x = df.drop("price_usd", axis=1)
        new_data = new_data[x.columns]
        print("New data for prediction:", new_data)

        y = df["price_usd"]

        model = KNeighborsRegressor(n_neighbors=4)
        model.fit(x, y)

        tahmin = model.predict(new_data)[0]
        print(f"Predicted price: {round(tahmin, 2)}")
        return Response({
            "message": "KNN prediction successful",
            "price": round(tahmin, 2)
        })

    except Exception as e:
        return Response({"error": str(e)}, status=400)
