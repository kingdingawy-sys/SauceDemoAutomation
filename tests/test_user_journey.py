import pytest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.mark.parametrize("driver", ["firefox"], indirect=True)
def test_complete_user_journey_firefox(driver):
    # 1. Login
    login_page = LoginPage(driver)
    login_page.login("standard_user", "secret_sauce")
    assert login_page.is_logged_in() == True

    # 2. Go to products
    driver.get("https://www.saucedemo.com/inventory.html")

    # 3. Add product to cart
    products_page = ProductsPage(driver)
    products_page.add_product_to_cart(0)
    products_page.go_to_cart()

    # 4. In cart, click checkout
    cart_page = CartPage(driver)
    cart_page.wait_for_cart_to_load()
    cart_page.click_checkout()

    # 5. Fill checkout info
    checkout_page = CheckoutPage(driver)
    checkout_page.fill_checkout_info("Ibrahim", "Mohamed", "12345")
    checkout_page.click_continue()

    # 6. Finish checkout
    checkout_page.click_finish()

    # 7. Handle alert if present
    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
        print("Alert appeared and accepted (though unexpected in Firefox).")
    except:
        print("No alert appeared in Firefox (as expected).")

    # 8. Assert checkout complete
    assert checkout_page.is_checkout_complete() == True