from django.urls import path
from . import view

urlpatterns = [
    path(
        "predict_product_rf/",
        view.predict_with_saved_model,
        name="predict_with_saved_model",
    ),
   path("predict_product_lstm/",
        view.predict_with_lstm_model,
        name = "predict_product_lstm")
]