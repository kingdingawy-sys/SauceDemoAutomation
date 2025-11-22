import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import allure
import os
from datetime import datetime


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

    print(f"\n🚀 Starting {browser.upper()} browser...")

    if browser == "firefox":
        options = FirefoxOptions()

        # لو في CI/CD، شغّل headless
        if os.getenv("CI"):
            options.add_argument("--headless")

        options.set_preference("dom.disable_beforeunload", True)
        options.set_preference("dom.disable_open_during_load", False)

        driver = webdriver.Firefox(options=options)

    else:  # chrome
        chrome_options = ChromeOptions()

        # لو في CI/CD، شغّل headless
        if os.getenv("CI"):
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")

        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-notifications")

        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        }
        chrome_options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()

    print(f"✅ Browser started successfully!")

    yield driver

    print(f"\n🛑 Closing {browser.upper()} browser...")
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook للتقاط screenshot عند فشل الـ test
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get('driver')
        if driver:
            # إنشاء folder للـ screenshots
            screenshots_dir = "screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)

            # اسم الملف بالتاريخ والوقت
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"{item.name}_{timestamp}.png"
            screenshot_path = os.path.join(screenshots_dir, screenshot_name)

            # حفظ السكرينشوت
            driver.save_screenshot(screenshot_path)
            print(f"\n📸 Screenshot saved: {screenshot_path}")

            # إرفاق الـ screenshot بالـ Allure report
            try:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=screenshot_name,
                    attachment_type=allure.attachment_type.PNG
                )
                print(f"✅ Screenshot attached to Allure report")
            except Exception as e:
                print(f"⚠️ Could not attach screenshot to Allure: {e}")