from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.cart_item = (By.CLASS_NAME, "cart_item")
        self.checkout_button = (By.ID, "checkout")
        self.continue_shopping_btn = (By.ID, "continue-shopping")

    def wait_for_cart_to_load(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.cart_item)
        )

    def get_items_count(self):
        return len(self.driver.find_elements(*self.cart_item))

    def click_continue_shopping(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.continue_shopping_btn)
        ).click()

    def click_checkout(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.checkout_button)
        ).click()

    def get_first_item_name(self):
        # نرجع اسم أول عنصر في السلة (لو موجود)
        items = self.driver.find_elements(*self.cart_item)
        if not items:
            return ""
        return items[0].find_element(By.CLASS_NAME, "inventory_item_name").text

    def remove_first_item(self):
        # استدعاء الزر الخاص بالإزالة لأول عنصر في الكارت
        remove_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button.cart_button, button.cart_quantity_delete")
        if remove_buttons:
            remove_buttons[0].click()
        else:
            raise Exception("No remove button found")