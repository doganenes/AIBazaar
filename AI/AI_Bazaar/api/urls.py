from django.urls import path
from . import view

urlpatterns = [
    path(
        "predict_product_rf/",
        view.predict_with_saved_model,
        name="predict_with_saved_model",
    ),
    path(
        "predict_with_saved_model/",
        view.predict_with_saved_model,
        name = "predict_with_saved_model/",
    ),

    path(
        "predict_product_lstm2/",
        view.predict_product_lstm,
        name="predict_product_lstm2",
    ),
   
   path(
       "predict_price/",
       view.predict_price,
       name = "predict_price"
   ),
   path("predict_product_lstm/",
        view.predict_with_lstm_model,
        name = "predict_product_lstm")
]