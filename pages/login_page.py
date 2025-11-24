from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:

    def __init__(self, driver):
        self.driver = driver

        # Locators
        self.username_input = (By.ID, "user-name")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "login-button")
        self.error_message = (By.CSS_SELECTOR, "h3[data-test='error']")

    def login(self, username, password):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located(self.username_input)).send_keys(username)
        wait.until(EC.visibility_of_element_located(self.password_input)).send_keys(password)
        wait.until(EC.element_to_be_clickable(self.login_button)).click()

    def get_error_message(self):
        wait = WebDriverWait(self.driver, 5)
        try:
            return wait.until(EC.visibility_of_element_located(self.error_message)).text
        except:
            return ""

    def is_logged_in(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
            )
            return True
        except:
            return False

    def is_locked_out_error(self):
        try:
            error_message = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
            )
            return "locked out" in error_message.text.lower()
        except:
            return False

    def has_broken_images(self):
        broken_images = self.driver.execute_script(
            "return Array.from(document.images).filter(img => !img.complete).length"
        )
        return broken_images > 0

    def is_page_loaded_quickly(self):
        import time
        start_time = time.time()
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
            )
            end_time = time.time()
            load_time = end_time - start_time
            return load_time < 5
        except:
            return False