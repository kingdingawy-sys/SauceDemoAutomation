from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.cart_item = (By.CLASS_NAME, "cart_item")
        self.cart_list = (By.CLASS_NAME, "cart_list")
        self.checkout_button = (By.ID, "checkout")
        self.continue_shopping_btn = (By.ID, "continue-shopping")

    def wait_for_cart_to_load(self, timeout=10):
        """Wait for cart page to load"""
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.cart_list)
        )
        time.sleep(0.5)  # Extra wait for rendering

    def get_items_count(self):
        return len(self.driver.find_elements(*self.cart_item))

    def click_continue_shopping(self):
        """Click continue shopping button"""
        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.continue_shopping_btn)
        )
        # 🔥 Scroll to button
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        time.sleep(0.3)
        btn.click()
        # 🔥 Wait for navigation
        time.sleep(1)

    def click_checkout(self):
        """Click checkout button"""
        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.checkout_button)
        )
        # 🔥 Scroll to button
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        time.sleep(0.3)
        btn.click()
        # 🔥 Wait for navigation
        time.sleep(1)

    def get_first_item_name(self):
        items = self.driver.find_elements(*self.cart_item)
        if not items:
            return ""
        return items[0].find_element(By.CLASS_NAME, "inventory_item_name").text

    def remove_first_item(self):
        """Remove first item from cart"""
        # 🔥 Find remove button for first item
        remove_btn = self.driver.find_element(By.CSS_SELECTOR, "button[id^='remove-']")

        # 🔥 Scroll to button
        self.driver.execute_script("arguments[0].scrollIntoView(true);", remove_btn)
        time.sleep(0.3)

        # Click
        remove_btn.click()

        # 🔥 Wait for item to be removed
        time.sleep(1)