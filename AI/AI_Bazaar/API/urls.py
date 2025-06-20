from django.urls import path
from . import views

urlpatterns = [
    path(
        "predict_product_xgboost/",
        views.predict_product_xgboost,
        name="predict_product_xgboost",
    ),
    # path(
    #     "predict_product_lstm/", views.predict_product_lstm, name="predict_product_lstm"
    # ),
]
