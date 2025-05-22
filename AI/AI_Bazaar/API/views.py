from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Basit GET API
def hello_api(request):
    data = {
        "message": "Merhaba, AI_Bazaar API çalışıyor!",
        "status": "success",
        "version": "1.0"
    }
    return JsonResponse(data)

# Ürün listesi API
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
    
    return JsonResponse({
        "status": "success",
        "count": len(products),
        "products": products
    })

# Tek ürün detayı API
def product_detail(request, product_id):
    # Basit örnek - gerçekte veritabanından gelecek
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
    
    return JsonResponse({
        "status": "success",
        "product": product
    })

# POST isteği kabul eden API
@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Basit validasyon
            required_fields = ['name', 'description', 'price']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({
                        "status": "error",
                        "message": f"'{field}' alanı gerekli"
                    }, status=400)
            
            # Burada normalde veritabanına kaydedilir
            new_product = {
                "id": 999,  # Gerçekte otomatik ID
                "name": data['name'],
                "description": data['description'],
                "price": data['price'],
                "created_at": "2024-01-01T00:00:00Z"
            }
            
            return JsonResponse({
                "status": "success",
                "message": "Ürün başarıyla oluşturuldu",
                "product": new_product
            }, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({
                "status": "error",
                "message": "Geçersiz JSON formatı"
            }, status=400)
    
    return JsonResponse({
        "status": "error",
        "message": "Sadece POST istekleri kabul edilir"
    }, status=405)

# API status kontrolü
def api_status(request):
    return JsonResponse({
        "status": "online",
        "service": "AI_Bazaar API",
        "endpoints": [
            "/api/hello/",
            "/api/products/",
            "/api/products/<id>/",
            "/api/products/create/",
            "/api/status/"
        ]
    })