from django.urls import path
from . import views

urlpatterns = [
    path(
        "predict_product_rf/",
        views.predict_with_saved_model,
        name="predict_with_saved_model",
    ),
    path(
        "predict_with_saved_model/",
        views.predict_with_saved_model,
        name = "predict_with_saved_model/",
    ),

#     path(
#         "predict_product_lstm/",
#         views.predict_product_lstm,
#         name="predict_product_lstm",
#     ),
   
#    path(
#        "predict_price/",
#        views.predict_price,
#        name = "predict_price"
#    )
]