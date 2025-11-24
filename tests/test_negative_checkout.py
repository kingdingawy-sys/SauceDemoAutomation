import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from selenium.webdriver.common.by import By


@pytest.mark.parametrize("driver", ["firefox"], indirect=True)
class TestNegativeCheckout:
    """
    Negative test cases for checkout flow
    """

    def setup_method(self):
        """Setup that runs before each test"""
        pass

    def add_product_and_go_to_checkout(self, driver):
        """Helper method to add product and navigate to checkout"""
        login = LoginPage(driver)
        login.login("standard_user", "secret_sauce")

        products = ProductsPage(driver)
        products.wait_for_page_to_load()
        products.add_product_to_cart(0)
        products.go_to_cart()

        cart = CartPage(driver)
        cart.wait_for_cart_to_load()
        cart.click_checkout()

    #  Test 1: Empty First Name
    def test_checkout_without_first_name(self, driver):
        """
        Test checkout fails when first name is missing
        """
        self.add_product_and_go_to_checkout(driver)

        checkout = CheckoutPage(driver)

        # Leave first name empty, fill others
        driver.find_element(By.ID, "last-name").send_keys("Mohamed")
        driver.find_element(By.ID, "postal-code").send_keys("12345")

        checkout.click_continue()

        #  Verify error message appears
        error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        assert error.is_displayed(), "Error message not displayed!"
        assert "First Name is required" in error.text or "Error" in error.text

        #  Verify still on step-one
        assert "checkout-step-one" in driver.current_url

        print(" Test passed: Checkout blocked without first name")

    #  Test 2: Empty Last Name
    def test_checkout_without_last_name(self, driver):
        """
        Test checkout fails when last name is missing
        """
        self.add_product_and_go_to_checkout(driver)

        checkout = CheckoutPage(driver)

        driver.find_element(By.ID, "first-name").send_keys("Ibrahim")
        # Leave last name empty
        driver.find_element(By.ID, "postal-code").send_keys("12345")

        checkout.click_continue()

        error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        assert error.is_displayed()
        assert "Last Name is required" in error.text or "Error" in error.text

        assert "checkout-step-one" in driver.current_url

        print(" Test passed: Checkout blocked without last name")

    #  Test 3: Empty Postal Code
    def test_checkout_without_postal_code(self, driver):
        """
        Test checkout fails when postal code is missing
        """
        self.add_product_and_go_to_checkout(driver)

        checkout = CheckoutPage(driver)

        driver.find_element(By.ID, "first-name").send_keys("Ibrahim")
        driver.find_element(By.ID, "last-name").send_keys("Mohamed")
        # Leave postal code empty

        checkout.click_continue()

        error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        assert error.is_displayed()
        assert "Postal Code is required" in error.text or "Error" in error.text

        assert "checkout-step-one" in driver.current_url

        print(" Test passed: Checkout blocked without postal code")

    #  Test 4: All Fields Empty
    def test_checkout_with_all_fields_empty(self, driver):
        """
        Test checkout fails when all fields are empty
        """
        self.add_product_and_go_to_checkout(driver)

        checkout = CheckoutPage(driver)

        # Don't fill anything, just click continue
        checkout.click_continue()

        error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        assert error.is_displayed()
        assert "Error" in error.text or "required" in error.text.lower()

        assert "checkout-step-one" in driver.current_url

        print(" Test passed: Checkout blocked with all empty fields")

    #  Test 5: Error Message Can Be Dismissed
    def test_error_message_can_be_dismissed(self, driver):
        """
        Test that error message has close button and can be dismissed
        """
        self.add_product_and_go_to_checkout(driver)

        checkout = CheckoutPage(driver)
        checkout.click_continue()  # Trigger error

        # Find error container
        error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        assert error.is_displayed()

        # Find and click close button
        close_btn = driver.find_element(By.CLASS_NAME, "error-button")
        close_btn.click()

        # Verify error is gone
        from selenium.common.exceptions import NoSuchElementException
        try:
            driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
            assert False, "Error message still visible after closing"
        except NoSuchElementException:
            print(" Test passed: Error message dismissed successfully")

    #  Test 6: Cancel Checkout
    def test_cancel_checkout_from_step_one(self, driver):
        """
        Test canceling checkout returns to cart
        """
        self.add_product_and_go_to_checkout(driver)

        # Click cancel button
        cancel_btn = driver.find_element(By.ID, "cancel")
        cancel_btn.click()

        # Should return to cart
        assert "cart" in driver.current_url

        print(" Test passed: Cancel returns to cart")

    #  Test 7: Cancel from Step Two
    def test_cancel_checkout_from_step_two(self, driver):
        """
        Test canceling from overview page returns to products
        """
        self.add_product_and_go_to_checkout(driver)

        checkout = CheckoutPage(driver)
        checkout.fill_checkout_info("Ibrahim", "Mohamed", "12345")
        checkout.click_continue()

        # Now on step-two, click cancel
        cancel_btn = driver.find_element(By.ID, "cancel")
        cancel_btn.click()

        # Should return to products page
        assert "inventory" in driver.current_url

        print(" Test passed: Cancel from step-two returns to inventory")


#  Separate test for empty cart (can't use the same setup)
@pytest.mark.parametrize("driver", ["firefox"], indirect=True)
def test_checkout_with_empty_cart(driver):
    """
    Test that checkout button is not accessible with empty cart
    OR verify appropriate behavior
    """
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    products = ProductsPage(driver)
    products.wait_for_page_to_load()

    # Go directly to cart without adding products
    products.go_to_cart()



    from selenium.common.exceptions import NoSuchElementException

    try:
        checkout_btn = driver.find_element(By.ID, "checkout")
        # If button exists, it might be disabled or clicking might show error
        # Let's check if we can click it
        is_enabled = checkout_btn.is_enabled()

        if is_enabled:
            # Click and see what happens
            checkout_btn.click()
            # Some sites allow this but show error later
            print(" Checkout button clickable with empty cart")
        else:
            print(" Test passed: Checkout button disabled with empty cart")

    except NoSuchElementException:
        print(" Test passed: Checkout button not present with empty cart")


#  Test 8: Special Characters in Fields
@pytest.mark.parametrize("driver", ["firefox"], indirect=True)
def test_checkout_with_special_characters(driver):
    """
    Test checkout with special characters in name fields
    """
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    products = ProductsPage(driver)
    products.wait_for_page_to_load()
    products.add_product_to_cart(0)
    products.go_to_cart()

    cart = CartPage(driver)
    cart.wait_for_cart_to_load()
    cart.click_checkout()

    checkout = CheckoutPage(driver)

    # Try special characters
    checkout.fill_checkout_info("@#$%^&*", "()<>?/", "!@#$%")
    checkout.click_continue()

    # Check if it proceeds or shows error
    # This depends on site's validation rules
    if "checkout-step-two" in driver.current_url:
        print(" Site accepts special characters in names")
        # Continue to verify checkout still works
        checkout.click_finish()
        assert checkout.is_checkout_complete()
        print(" Checkout completed with special characters")
    else:
        # Error should appear
        error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        assert error.is_displayed()
        print(" Site blocks special characters appropriately")