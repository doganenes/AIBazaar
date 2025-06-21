from django.urls import path
from . import views

urlpatterns = [
    path(
        "predict_product_xgboost/",
        views.predict_product_xgboost,
        name="predict_product_xgboost",
    ),
    
]
