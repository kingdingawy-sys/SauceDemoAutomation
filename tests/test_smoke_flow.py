"""from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage

def test_full_smoke_flow(driver):
    # Login
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    # Products Page
    products = ProductsPage(driver)
    products.wait_for_page_to_load()
    products.add_backpack_to_cart()
    products.go_to_cart()

    # Cart Page
    cart = CartPage(driver)
    cart.wait_for_cart_to_load()

    # assert
    assert cart.get_items_count() == 1
"""