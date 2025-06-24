from django.urls import path
from . import views

urlpatterns = [
    path(
        "predict_product_rf/",
        views.predict_product_rf,
        name="predict_product_rf",
    ),

   
]
