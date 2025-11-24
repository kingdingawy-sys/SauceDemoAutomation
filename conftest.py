import allure
import pytest
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser: chrome, chromium, or firefox"
    )


@pytest.fixture
def driver(request):
    browser = getattr(request, "param", request.config.getoption("--browser"))

    is_ci = bool(os.getenv("CI") or os.getenv("GITHUB_ACTIONS"))
    print(f"\n Starting {browser.upper()} browser (CI: {is_ci})")

    if browser.lower() == "firefox":
        options = FirefoxOptions()
        options.set_preference("dom.disable_beforeunload", True)
        options.set_preference("dom.disable_open_during_load", False)

        if is_ci:
            options.add_argument("--headless")

        driver = webdriver.Firefox(options=options)

    else:
        options = ChromeOptions()

        # Basic settings
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--window-size=1920,1080")

        # CI-only settings (Chromium)
        if is_ci:
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")

            #  Set Chromium binary location
            options.binary_location = "/usr/bin/chromium-browser"

            #  Use Service instead of executable_path
            service = ChromeService(executable_path="/usr/lib/chromium-browser/chromedriver")
            driver = webdriver.Chrome(service=service, options=options)

        else:
            prefs = {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False
            }
            options.add_experimental_option("prefs", prefs)

            driver = webdriver.Chrome(options=options)

    driver.get("https://www.saucedemo.com/")
    time.sleep(0.7)

    yield driver
    driver.quit()


# Screenshot on failure
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