import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

@pytest.mark.parametrize("driver", ["firefox"], indirect=True)
def test_checkout_flow(driver):
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    products = ProductsPage(driver)
    products.add_product_to_cart(0)
    products.go_to_cart()

    cart = CartPage(driver)
    cart.wait_for_cart_to_load()
    cart.click_checkout()

    checkout = CheckoutPage(driver)
    checkout.fill_checkout_info("Ibrahim", "Mohamed", "12345")
    checkout.click_continue()
    checkout.click_finish()

    assert checkout.is_checkout_complete()
