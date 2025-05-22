from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello_api, name='hello_api'),
    
    path('products/', views.product_list, name='product_list'),
    
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    
    path('products/create/', views.create_product, name='create_product'),
    
    path('status/', views.api_status, name='api_status'),
]