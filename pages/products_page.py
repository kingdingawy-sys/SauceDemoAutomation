from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProductsPage:
    def __init__(self, driver):
        self.driver = driver
        self.page_title = (By.CLASS_NAME, "title")
        self.products_list = (By.CLASS_NAME, "inventory_item")
        self.add_buttons = (By.CLASS_NAME, "btn_inventory")
        self.cart_icon = (By.CLASS_NAME, "shopping_cart_link")
        self.sort_dropdown = (By.CLASS_NAME, "product_sort_container")

    def wait_for_page_to_load(self, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.page_title)
        )

    def get_products_count(self):
        return len(self.driver.find_elements(*self.products_list))

    def toggle_product_in_cart(self, index=0, expected_text="Remove", timeout=5):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(self.add_buttons)
        )
        buttons = self.driver.find_elements(*self.add_buttons)
        button = buttons[index]

        if button.text.strip().lower() != expected_text.lower():
            button.click()

        WebDriverWait(self.driver, timeout).until(
            lambda d: d.find_elements(*self.add_buttons)[index].text.strip().lower() == expected_text.lower()
        )
        return self.driver.find_elements(*self.add_buttons)[index].text

    def add_product_to_cart(self, index=0, timeout=5):
        return self.toggle_product_in_cart(index=index, expected_text="Remove", timeout=timeout)

    def remove_product_from_cart(self, index=0, timeout=5):
        return self.toggle_product_in_cart(index=index, expected_text="Add to cart", timeout=timeout)

    def get_cart_count(self):
        try:
            badge = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
            return int(badge.text)
        except Exception:
            return 0

    def go_to_cart(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(self.cart_icon)
        ).click()

    def open_product_details(self, index=0, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(self.products_list)
        )
        items = self.driver.find_elements(*self.products_list)
        items[index].find_element(By.CLASS_NAME, "inventory_item_name").click()

    def sort_products(self, sort_option_text):
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.sort_dropdown)
        )
        dropdown.click()
        opt = dropdown.find_element(By.XPATH, f".//option[text()='{sort_option_text}']")
        opt.click()

    def get_product_name(self, index):
        products = self.driver.find_elements(
            By.CLASS_NAME,
            "inventory_item"
        )
        return products[index].find_element(By.CLASS_NAME, "inventory_item_name").text

