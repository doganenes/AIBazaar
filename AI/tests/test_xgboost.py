import pytest
from rest_framework.test import APIRequestFactory
from your_app.views import predict_product_xgboost

# Gerekli örnek veri
sample_data = {
    "ram": 8,
    "storage": 128,
    "display_size": 6.5,
    "battery": 4500,
    "quick_charge": 1,
    "ppi": 400,
    "os_type": "Android",
    "display_type": "AMOLED",
    "camera": 48.0,
    "chipset": 7
}

@pytest.mark.django_db
def test_predict_product_xgboost_success():
    factory = APIRequestFactory()
    request = factory.post("/predict/", sample_data, format="json")

    response = predict_product_xgboost(request)

    assert response.status_code == 200
    assert "price" in response.data
    assert "message" in response.data
    assert response.data["message"] == "XGBoost prediction successful"

@pytest.mark.django_db
def test_predict_product_xgboost_missing_field():
    faulty_data = sample_data.copy()
    del faulty_data["ram"]  # Önemli bir alanı sil

    factory = APIRequestFactory()
    request = factory.post("/predict/", faulty_data, format="json")

    response = predict_product_xgboost(request)

    assert response.status_code == 400
    assert "error" in response.data
