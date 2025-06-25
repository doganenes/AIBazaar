from django.urls import path
from . import views

urlpatterns = [
    path(
        "predict_product_rf/",
        views.predict_with_saved_model,
        name="predict_with_saved_model",
    ),
    path(
        "predict_product_rf/",
        views.predict_product_rf,
        name="predict_product_rf",
    ),
    path(
        "train_and_save_model/",
        views.train_and_save_model,
        name="train_and_save_model",
    ),
    path("list_saved_models/", views.list_saved_models, name="list_saved_models"),
    # path(
    #     "predict_product_lstm/",
    #     views.predict_product_lstm,
    #     name="predict_product_lstm",
    # ),
]
