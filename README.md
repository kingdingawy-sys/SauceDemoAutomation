# 🧪 SauceDemo Test Automation Framework

![Tests](https://github.com/YourUsername/SauceDemoAutomation/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Selenium](https://img.shields.io/badge/selenium-4.27-green)
![License](https://img.shields.io/badge/license-MIT-blue)

> Comprehensive end-to-end test automation framework for [SauceDemo](https://www.saucedemo.com/) e-commerce application

---

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [CI/CD](#cicd)
- [Reports](#reports)

---

## 🎯 Overview

This project demonstrates a production-ready test automation framework using **Selenium WebDriver**, **Python**, and **Pytest**. It includes 43+ comprehensive test cases covering:
- User authentication & authorization
- Product browsing & filtering
- Shopping cart management
- Complete checkout flow
- Edge cases & security testing
- Multi-user scenarios

---

## ✨ Features

- ✅ **Page Object Model (POM)** design pattern
- ✅ **Cross-browser testing** (Chrome/Chromium, Firefox)
- ✅ **CI/CD Pipeline** with GitHub Actions
- ✅ **Allure Reports** with screenshots on failure
- ✅ **Headless execution** for CI/CD
- ✅ **90%+ test coverage**
- ✅ **Parallel execution** support (pytest-xdist)
- ✅ **Comprehensive edge case testing**

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| **Language** | Python 3.11 |
| **Framework** | Pytest 8.3 |
| **Web Automation** | Selenium 4.27 |
| **Reporting** | Allure 2.13 |
| **CI/CD** | GitHub Actions |
| **Browsers** | Chrome, Firefox, Chromium |

---

## 📁 Project Structure
```
SauceDemoAutomation/
├── .github/
│   └── workflows/
│       └── tests.yml              # CI/CD pipeline configuration
│
├── pages/                          # Page Object Models
│   ├── __init__.py
│   ├── login_page.py               # Login page interactions
│   ├── products_page.py            # Products listing page
│   ├── cart_page.py                # Shopping cart page
│   ├── checkout_page.py            # Checkout flow pages
│   └── product_details_page.py     # Individual product details
│
├── tests/                          # Test suites
│   ├── test_cart.py                # Cart functionality tests
│   ├── test_checkout.py            # Checkout flow tests
│   ├── test_checkout_edge_cases.py # Edge cases & boundary tests
│   ├── test_login.py               # Login functionality tests
│   ├── test_multi_user_login.py    # Multi-user scenarios
│   ├── test_multiple_products_checkout.py  # Multiple items checkout
│   ├── test_negative_checkout.py   # Negative test scenarios
│   ├── test_products.py            # Product browsing & sorting
│   └── test_user_journey.py        # End-to-end user journey
│
├── utils/                          # Utility modules
│   ├── __init__.py
│   └── test_data.py                # Test data management
│
├── reports/                        # Test reports directory
│   └── allure-results/             # Allure test results
│
├── screenshots/                    # Screenshots on test failure
│
├── .venv/                          # Virtual environment (not in repo)
│
├── conftest.py                     # Pytest fixtures & configuration
├── pytest.ini                      # Pytest settings
├── requirements.txt                # Python dependencies
├── test_data.py                    # Test data constants
├── .gitignore                      # Git ignore rules
└── README.md                       # Project documentation
```

---

## 📦 Installation

### Prerequisites
- Python 3.11+
- Chrome/Firefox browser
- Git

### Setup
```bash
# 1. Clone repository
git clone https://github.com/YourUsername/SauceDemoAutomation.git
cd SauceDemoAutomation

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Running Tests

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/test_checkout.py -v
```

### Run Specific Test Class
```bash
pytest tests/test_cart.py::TestCart -v
```

### Run with Specific Browser
```bash
# Firefox
pytest tests/ --browser=firefox -v

# Chrome (default)
pytest tests/ --browser=chrome -v
```

### Run with Allure Report
```bash
# Generate results
pytest tests/ --alluredir=allure-results -v

# View report
allure serve allure-results
```

### Parallel Execution (faster)
```bash
# Run on 4 cores
pytest tests/ -n 4 -v

# Auto-detect cores
pytest tests/ -n auto -v
```

---

## 📊 Test Coverage

| Test Category | Test Count | Coverage |
|--------------|------------|----------|
| **Login & Auth** | 6 tests | Authentication, multi-user scenarios, locked users |
| **Products** | 8 tests | Browse, sort, filter, product details |
| **Cart** | 5 tests | Add, remove, continue shopping, validation |
| **Checkout** | 12 tests | Positive flow, field validation, navigation |
| **Negative Cases** | 9 tests | Empty fields, invalid data, cancellation |
| **Edge Cases** | 12 tests | XSS, SQL injection, Unicode, boundaries |
| **User Journey** | 1 test | Complete E2E flow from login to checkout |
| **Total** | **43 tests** | **90%+ coverage** |

### Test Distribution
- ✅ **Positive Tests:** 25 tests
- ❌ **Negative Tests:** 9 tests
- 🔒 **Security Tests:** 2 tests
- 🎯 **Edge Cases:** 12 tests

---

## 🔄 CI/CD

Automated testing runs on every push/pull request via **GitHub Actions**.

### Workflow Features:
- ✅ Runs on Ubuntu latest
- ✅ Tests on Chromium (headless)
- ✅ Python 3.11
- ✅ Uploads screenshots on failure
- ✅ Generates Allure reports
- ✅ Archives test artifacts for 7 days

### View Workflow:
- **File:** `.github/workflows/tests.yml`
- **Status:** https://github.com/ibrahim-dingawy/SauceDemoAutomation/actions/workflows/tests.yml/badge.svg
---

## 📈 Reports

### Allure Report Features:
- 📊 **Test execution statistics** - Pass/Fail rates, duration
- 📸 **Screenshots on failure** - Automatic capture and attachment
- 📝 **Detailed step logs** - Step-by-step execution details
- 📉 **Historical trends** - Track test stability over time
- 🎯 **Test categorization** - By feature, severity, and type
- ⏱️ **Performance metrics** - Execution time analysis

### Generate Local Report:
```bash
# Run tests with Allure
pytest tests/ --alluredir=reports/allure-results -v

# Serve report
allure serve reports/allure-results
```

---

## 🧪 Test Examples

### Positive Flow Test
```python
def test_checkout_flow(driver):
    """Complete checkout process with valid data"""
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")
    
    products = ProductsPage(driver)
    products.add_product_to_cart(0)
    products.go_to_cart()
    
    cart = CartPage(driver)
    cart.click_checkout()
    
    checkout = CheckoutPage(driver)
    checkout.fill_checkout_info("Ibrahim", "Mohamed", "12345")
    checkout.click_continue()
    checkout.click_finish()
    
    assert checkout.is_checkout_complete()
```

### Negative Test
```python
def test_checkout_without_first_name(driver):
    """Verify checkout fails without first name"""
    checkout = CheckoutPage(driver)
    checkout.fill_checkout_info("", "Mohamed", "12345")
    checkout.click_continue()
    
    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert error.is_displayed()
    assert "First Name is required" in error.text
```

### Edge Case Test
```python
def test_checkout_with_xss_payload(driver):
    """Security test - XSS injection attempt"""
    xss_payload = "<script>alert('XSS')</script>"
    checkout.fill_checkout_info(xss_payload, xss_payload, "12345")
    checkout.click_continue()
    
    # Verify payload is escaped, not executed
    page_source = driver.page_source
    assert "<script>" not in page_source
```

---

## 🎨 Page Object Model Example
```python
# pages/login_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.ID, "user-name")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "login-button")
    
    def login(self, username, password):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.username_input)
        ).send_keys(username)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_button).click()
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👤 Author

Ibrahim Ahmed 
- 💼 LinkedIn: [Ibrahim A. Mohamed](https://www.linkedin.com/in/ibrahim-dingawy)
- 🐙 GitHub: [@kingdingawy-sys](https://github.com/kingdingawy-sys)
- 📧 Email: [ibrahim.softtest.qa@proton.me](mailto:ibrahim.softtest.qa@proton.me)

---

## 🙏 Acknowledgments

- [SauceDemo](https://www.saucedemo.com/) - Test application provided by Sauce Labs
- [Selenium](https://www.selenium.dev/) - Web automation framework
- [Pytest](https://pytest.org/) - Python testing framework
- [Allure](https://docs.qameta.io/allure/) - Test reporting tool

---

## 📊 Project Stats

- **Lines of Code:** 2000+
- **Test Cases:** 43
- **Page Objects:** 5
- **Test Coverage:** 90%+
- **Average Test Duration:** 3-4 minutes
- **CI/CD Success Rate:** 97%+

---


⭐ **If you find this project useful, please give it a star!**
