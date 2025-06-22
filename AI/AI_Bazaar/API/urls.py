from django.urls import path
from . import views

urlpatterns = [
    path(
        "predict_product_rf/",
        views.predict_product_rf,
        name="predict_product_rf",
    ),

    path(
        "predict_product_lstm/",
        views.predict_product_lstm,
        name="predict_product_lstm",
    ),
]
