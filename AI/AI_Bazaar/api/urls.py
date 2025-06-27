from django.urls import path
from . import view

urlpatterns = [
    path(
        "predict_product_rf/",
        view.predict_product_rf,
        name="predict_product_rf",
    ),
   path("predict_product_lstm/",
        view.predict_with_lstm_model,
        name = "predict_product_lstm")
]