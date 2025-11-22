import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from selenium.webdriver.common.by import By

def test_cart_loads(driver):
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    products = ProductsPage(driver)
    products.add_product_to_cart(0)
    products.go_to_cart()

    cart = CartPage(driver)
    cart.wait_for_cart_to_load()

    # الصفحة فتحت وظهر عنصر واحد
    assert cart.get_items_count() == 1


def test_remove_item_from_cart(driver):
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    products = ProductsPage(driver)
    products.add_product_to_cart(0)
    products.go_to_cart()

    cart = CartPage(driver)
    cart.wait_for_cart_to_load()

    # إزالة أول عنصر
    cart.remove_first_item()

    assert cart.get_items_count() == 0


def test_continue_shopping(driver):
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    products = ProductsPage(driver)
    products.add_product_to_cart(0)
    products.go_to_cart()

    cart = CartPage(driver)
    cart.wait_for_cart_to_load()

    cart.click_continue_shopping()

    assert "inventory.html" in driver.current_url


def test_checkout_button(driver):
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    products = ProductsPage(driver)
    products.add_product_to_cart(0)
    products.go_to_cart()

    cart = CartPage(driver)
    cart.wait_for_cart_to_load()

    cart.click_checkout()

    assert "checkout-step-one.html" in driver.current_url


def test_cart_item_name_matches_products(driver):
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    products = ProductsPage(driver)

    # اسم أول منتج في صفحة المنتجات
    product_name = products.get_product_name(0)

    products.add_product_to_cart(0)
    products.go_to_cart()

    cart = CartPage(driver)
    cart.wait_for_cart_to_load()

    # اسم المنتج في الكارت
    cart_name = cart.get_first_item_name()

    assert product_name == cart_name
