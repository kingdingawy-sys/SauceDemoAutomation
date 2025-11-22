from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.first_name_input = (By.ID, "first-name")
        self.last_name_input = (By.ID, "last-name")
        self.postal_code_input = (By.ID, "postal-code")
        self.continue_btn = (By.ID, "continue")
        self.finish_btn = (By.ID, "finish")
        self.complete_header = (By.CLASS_NAME, "complete-header")

    def fill_checkout_info(self, first, last, postal):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.first_name_input)
        ).send_keys(first)
        self.driver.find_element(*self.last_name_input).send_keys(last)
        self.driver.find_element(*self.postal_code_input).send_keys(postal)

    def click_continue(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.continue_btn)
        ).click()

    def click_finish(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.finish_btn)
        ).click()

    def is_checkout_complete(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.complete_header)
        ).is_displayed()
