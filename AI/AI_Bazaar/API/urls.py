from django.urls import path
from . import views

urlpatterns = [
    path("predict_product_knn/", views.predict_product_knn, name="predict_product_knn"),
    path("predict_product_lstm/", views.predict_product_lstm, name="predict_product_lstm"),
]