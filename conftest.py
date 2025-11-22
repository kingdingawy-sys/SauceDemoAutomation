import allure
import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService


def pytest_addoption(parser):
    """إضافة browser option"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser: chrome or firefox"
    )


@pytest.fixture
def driver(request):
    """
    Driver fixture - يشتغل محلياً وفي CI/CD
    """
    # Get browser from parametrize OR command line
    if hasattr(request, "param"):
        browser = request.param
    else:
        browser = request.config.getoption("--browser")

    # Check if running in CI
    is_ci = os.getenv("CI") or os.getenv("GITHUB_ACTIONS")

    print(f"\n🚀 Starting {browser.upper()} browser (CI: {bool(is_ci)})")

    if browser.lower() == "firefox":
        options = FirefoxOptions()
        options.set_preference("dom.disable_beforeunload", True)
        options.set_preference("dom.disable_open_during_load", False)

        if is_ci:
            options.add_argument("--headless")

        driver = webdriver.Firefox(options=options)

    else:  # chrome (default)
        options = ChromeOptions()
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")

        if is_ci:
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")

        options.add_argument("--window-size=1920,1080")

        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        }
        options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(options=options)

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
            os.makedirs("screenshots", exist_ok=True)
            screenshot_path = f"screenshots/{item.name}.png"
            driver.save_screenshot(screenshot_path)

            try:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=item.name,
                    attachment_type=allure.attachment_type.PNG
                )
            except:
                pass