from django.urls import path
from . import views

urlpatterns = [
   
   path("predict_product_lstm/",
        views.predict_with_lstm_model,
        name = "predict_product_lstm"),
   
    path("predict_product_rf/", 
         views.predict_phone_price, 
         name="predict_phone_price")
]