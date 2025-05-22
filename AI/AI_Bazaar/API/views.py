from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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