from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProductDetailsPage:
    def __init__(self, driver):
        self.driver = driver
        self.title = (By.CLASS_NAME, "inventory_details_name")
        self.description = (By.CLASS_NAME, "inventory_details_desc")
        self.price = (By.CLASS_NAME, "inventory_details_price")
        self.back_button = (By.ID, "back-to-products")

    # ---- Details ----
    def get_title(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.title)
        ).text

    def get_description(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.description)
        ).text

    def get_price(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.price)
        ).text

    def click_back(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.back_button)
        ).click()
