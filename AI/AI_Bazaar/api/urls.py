from django.urls import path
from . import view

urlpatterns = [
   
   path("predict_product_lstm/",
        view.predict_with_lstm_model,
        name = "predict_product_lstm"),
   
    path("predict_phone_price/", 
         view.predict_phone_price, 
         name="predict_phone_price")
]