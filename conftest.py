import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import allure
import os


def pytest_addoption(parser):
    """إضافة option للـ browser"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests: chrome or firefox"
    )


@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")

    if browser == "firefox":
        options = FirefoxOptions()
        options.add_argument("--headless")  # يشتغل بدون UI في CI
        options.set_preference("dom.disable_beforeunload", True)
        driver = webdriver.Firefox(options=options)

    else:  # chrome
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")  # يشتغل بدون UI
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        }
        chrome_options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()

    yield driver

    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Screenshot on failure"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get('driver')
        if driver:
            # Create screenshots folder
            os.makedirs("screenshots", exist_ok=True)

            # Save screenshot
            screenshot_path = f"screenshots/{item.name}.png"
            driver.save_screenshot(screenshot_path)

            # Attach to Allure
            allure.attach(
                driver.get_screenshot_as_png(),
                name=item.name,
                attachment_type=allure.attachment_type.PNG
            )