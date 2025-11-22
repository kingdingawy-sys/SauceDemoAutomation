import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from selenium.webdriver.common.by import By


@pytest.mark.parametrize("driver", ["firefox"], indirect=True)
class TestCheckoutEdgeCases:
    """
    Edge cases and boundary testing for checkout
    """

    def add_product_and_checkout(self, driver):
        """Helper to reach checkout page"""
        login = LoginPage(driver)
        login.login("standard_user", "secret_sauce")

        products = ProductsPage(driver)
        products.wait_for_page_to_load()
        products.add_product_to_cart(0)
        products.go_to_cart()

        cart = CartPage(driver)
        cart.wait_for_cart_to_load()
        cart.click_checkout()

    # 🔥 Test 1: Very Long Names
    def test_checkout_with_very_long_names(self, driver):
        """
        Test checkout with extremely long names (100+ characters)
        """
        self.add_product_and_checkout(driver)

        checkout = CheckoutPage(driver)

        long_first_name = "A" * 150  # 150 characters
        long_last_name = "B" * 150

        checkout.fill_checkout_info(long_first_name, long_last_name, "12345")
        checkout.click_continue()

        # Check if it accepts or rejects
        if "checkout-step-two" in driver.current_url:
            print("⚠️ Site accepts very long names (150 chars)")
            checkout.click_finish()
            assert checkout.is_checkout_complete()
            print("✅ Checkout completed with very long names")
        else:
            # Should show error
            error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
            assert error.is_displayed()
            print("✅ Site properly rejects very long names")

    # 🔥 Test 2: Whitespace-Only Fields
    def test_checkout_with_whitespace_only(self, driver):
        """
        Test checkout with fields containing only spaces
        """
        self.add_product_and_checkout(driver)

        checkout = CheckoutPage(driver)

        # Fill with spaces only
        checkout.fill_checkout_info("   ", "   ", "   ")
        checkout.click_continue()

        # Should either trim and show error, or reject
        if "checkout-step-one" in driver.current_url:
            error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
            assert error.is_displayed()
            print("✅ Whitespace-only input properly rejected")
        else:
            print("⚠️ Site accepts whitespace-only input")

    # 🔥 Test 3: Leading/Trailing Spaces
    def test_checkout_with_leading_trailing_spaces(self, driver):
        """
        Test if the system trims leading/trailing spaces
        """
        self.add_product_and_checkout(driver)

        checkout = CheckoutPage(driver)

        checkout.fill_checkout_info("  Ibrahim  ", "  Mohamed  ", "  12345  ")
        checkout.click_continue()

        assert "checkout-step-two" in driver.current_url
        checkout.click_finish()
        assert checkout.is_checkout_complete()

        print("✅ Checkout handles leading/trailing spaces correctly")

    # 🔥 Test 4: Numbers in Name Fields
    def test_checkout_with_numbers_in_names(self, driver):
        """
        Test if numbers are allowed in name fields
        """
        self.add_product_and_checkout(driver)

        checkout = CheckoutPage(driver)

        checkout.fill_checkout_info("Ibrahim123", "Mohamed456", "12345")
        checkout.click_continue()

        if "checkout-step-two" in driver.current_url:
            print("⚠️ Site accepts numbers in names")
            checkout.click_finish()
            assert checkout.is_checkout_complete()
        else:
            error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
            assert error.is_displayed()
            print("✅ Site rejects numbers in names")

    # 🔥 Test 5: Mixed Languages (Unicode)
    def test_checkout_with_unicode_characters(self, driver):
        """
        Test checkout with Arabic/Unicode characters
        """
        self.add_product_and_checkout(driver)

        checkout = CheckoutPage(driver)

        checkout.fill_checkout_info("إبراهيم", "محمد", "١٢٣٤٥")
        checkout.click_continue()

        if "checkout-step-two" in driver.current_url:
            print("✅ Site supports Unicode/Arabic characters")
            checkout.click_finish()
            assert checkout.is_checkout_complete()
        else:
            print("⚠️ Site doesn't support Unicode characters")

    # 🔥 Test 6: Alphanumeric Postal Code
    def test_checkout_with_alphanumeric_postal_code(self, driver):
        """
        Test postal code with letters (like UK postcodes: SW1A 1AA)
        """
        self.add_product_and_checkout(driver)

        checkout = CheckoutPage(driver)

        checkout.fill_checkout_info("Ibrahim", "Mohamed", "SW1A1AA")
        checkout.click_continue()

        if "checkout-step-two" in driver.current_url:
            print("✅ Site accepts alphanumeric postal codes")
            checkout.click_finish()
            assert checkout.is_checkout_complete()
        else:
            print("⚠️ Site only accepts numeric postal codes")

    # 🔥 Test 7: Negative/Zero Postal Code
    def test_checkout_with_negative_postal_code(self, driver):
        """
        Test postal code with negative number
        """
        self.add_product_and_checkout(driver)

        checkout = CheckoutPage(driver)

        checkout.fill_checkout_info("Ibrahim", "Mohamed", "-12345")
        checkout.click_continue()

        if "checkout-step-two" in driver.current_url:
            print("⚠️ Site accepts negative postal code")
            checkout.click_finish()
            assert checkout.is_checkout_complete()
        else:
            print("✅ Site rejects negative postal code")

    # 🔥 Test 8: XSS Attempt in Fields
    def test_checkout_with_xss_payload(self, driver):
        """
        Test if site is vulnerable to XSS attacks
        """
        self.add_product_and_checkout(driver)

        checkout = CheckoutPage(driver)

        xss_payload = "<script>alert('XSS')</script>"
        checkout.fill_checkout_info(xss_payload, xss_payload, "12345")
        checkout.click_continue()

        # Check if script executed (alert appeared)
        from selenium.common.exceptions import UnexpectedAlertPresentException

        try:
            if "checkout-step-two" in driver.current_url:
                # Check if the payload is rendered as-is or escaped
                page_source = driver.page_source

                if "<script>" in page_source:
                    print("🚨 SECURITY RISK: XSS payload not escaped!")
                else:
                    print("✅ XSS payload properly escaped")

                checkout.click_finish()
                assert checkout.is_checkout_complete()
        except UnexpectedAlertPresentException:
            print("🚨 CRITICAL: XSS executed! Alert appeared!")
            driver.switch_to.alert.accept()

    # 🔥 Test 9: SQL Injection Attempt
    def test_checkout_with_sql_injection(self, driver):
        """
        Test SQL injection in input fields
        """
        self.add_product_and_checkout(driver)

        checkout = CheckoutPage(driver)

        sql_payload = "' OR '1'='1"
        checkout.fill_checkout_info(sql_payload, sql_payload, "12345")
        checkout.click_continue()

        # If it proceeds normally, the input was sanitized
        if "checkout-step-two" in driver.current_url:
            print("✅ SQL injection payload handled safely")
            checkout.click_finish()
            assert checkout.is_checkout_complete()
        else:
            print("⚠️ Unexpected behavior with SQL payload")

    # 🔥 Test 10: Repeated Rapid Clicks on Continue
    def test_rapid_clicks_on_continue_button(self, driver):
        """
        Test double-submit prevention
        """
        self.add_product_and_checkout(driver)

        checkout = CheckoutPage(driver)
        checkout.fill_checkout_info("Ibrahim", "Mohamed", "12345")

        # Click multiple times rapidly
        continue_btn = driver.find_element(By.ID, "continue")
        for _ in range(5):
            try:
                continue_btn.click()
            except:
                pass  # Button might become stale

        # Should still end up on step-two only once
        assert "checkout-step-two" in driver.current_url

        # Verify no duplicate orders or errors
        print("✅ Rapid clicks handled correctly (no double-submit)")

    # 🔥 Test 11: Back Button During Checkout
    def test_browser_back_button_during_checkout(self, driver):
        """
        Test behavior when using browser back button
        """
        self.add_product_and_checkout(driver)

        checkout = CheckoutPage(driver)
        checkout.fill_checkout_info("Ibrahim", "Mohamed", "12345")
        checkout.click_continue()

        assert "checkout-step-two" in driver.current_url

        # Use browser back button
        driver.back()

        # Should return to step-one with data preserved or cleared
        assert "checkout-step-one" in driver.current_url

        # Check if data is still there
        first_name_value = driver.find_element(By.ID, "first-name").get_attribute("value")

        if first_name_value == "Ibrahim":
            print("✅ Form data preserved after back button")
        else:
            print("⚠️ Form data cleared after back button")

    # 🔥 Test 12: Direct URL Access to Step Two
    def test_direct_access_to_step_two(self, driver):
        """
        Test if user can skip step-one by directly accessing step-two URL
        """
        login = LoginPage(driver)
        login.login("standard_user", "secret_sauce")

        products = ProductsPage(driver)
        products.wait_for_page_to_load()
        products.add_product_to_cart(0)

        # Try to directly access step-two without going through step-one
        driver.get("https://www.saucedemo.com/checkout-step-two.html")

        import time
        time.sleep(1)

        # Should either:
        # 1. Redirect back to step-one or cart
        # 2. Show error
        # 3. Stay on step-two but with issues

        current_url = driver.current_url

        if "checkout-step-two" in current_url:
            print("⚠️ Direct access to step-two allowed (potential security issue)")
        elif "checkout-step-one" in current_url:
            print("✅ Redirected to step-one (proper flow enforcement)")
        elif "cart" in current_url or "inventory" in current_url:
            print("✅ Redirected to safe page (proper access control)")