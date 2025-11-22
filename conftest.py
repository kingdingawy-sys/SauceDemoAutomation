import allure
import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def pytest_addoption(parser):
    """
    إضافة option للـ browser من الـ command line
    """
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests: chrome or firefox"
    )


@pytest.fixture
def driver(request):
    """
    Driver fixture يشتغل محلياً وفي CI/CD
    """
    # جيب الـ browser من الـ parametrize أو من الـ command line
    if hasattr(request, "param"):
        browser = request.param
    else:
        browser = request.config.getoption("--browser")

    # تحديد إذا كنا في CI/CD environment
    is_ci = os.getenv("CI") or os.getenv("GITHUB_ACTIONS")

    if browser == "firefox":
        options = FirefoxOptions()
        options.set_preference("dom.disable_beforeunload", True)
        options.set_preference("dom.disable_open_during_load", False)

        # في CI/CD شغّل headless
        if is_ci:
            options.add_argument("--headless")

        driver = webdriver.Firefox(options=options)

    else:  # default = chrome
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")

        # في CI/CD، ضيف arguments إضافية
        if is_ci:
            chrome_options.add_argument("--headless")
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
    """
    Screenshot on failure
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get('driver')
        if driver:
            # إنشاء folder للـ screenshots
            os.makedirs("screenshots", exist_ok=True)

            # حفظ screenshot
            screenshot_path = f"screenshots/{item.name}.png"
            driver.save_screenshot(screenshot_path)

            # إرفاق بالـ Allure
            try:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=item.name,
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception:
                pass  # في حالة فشل الـ attach، استمر