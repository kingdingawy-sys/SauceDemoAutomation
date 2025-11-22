import requests
import pytest

def test_verify_login_api():
    """
    اختبار إن المستخدم *مافيش* يقدر يسجّل دخول باستخدام API (مافيش بيانات)
    """
    # البيانات اللي بنستخدمها
    login_data = {
        "email": "ibrahim.mahmoud@hotmail.com",
        "password": "123456789"
    }

    # نعمل call للـ API (endpoint صح)
    response = requests.post("https://automationexercise.com/api/verifyLogin", json=login_data)

    # نتاكد إن الـ status code = 400 (Bad Request)
    assert response.status_code == 400

    # نتاكد إن الـ response بيحوي رسالة خطأ
    assert response.json()["responseCode"] == 400

def test_get_products_api():
    """
    اختبار إن نقدر نجيب بيانات المنتجات
    """
    response = requests.get("https://automationexercise.com/api/productsList")

    assert response.status_code == 200
    assert len(response.json()) > 0  # مافيش مشكلة لو مالاقيش منتجات، بس لازم يكون في بيانات