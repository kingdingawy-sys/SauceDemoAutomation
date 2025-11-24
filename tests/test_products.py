import pytest
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.products_page import ProductsPage


def login_and_get_products(driver):
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")
    return ProductsPage(driver)


@pytest.mark.smoke
def test_products_page_load(driver):
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")
    assert "inventory.html" in driver.current_url


@pytest.mark.smoke
def test_add_remove_product(driver):
    products = login_and_get_products(driver)

    # Add first product
    button_text = products.add_product_to_cart(0)
    assert button_text == "Remove"

    # Remove first product
    button_text = products.remove_product_from_cart(0)
    assert button_text == "Add to cart"


def test_sort_by_price_low_to_high(driver):
    products = login_and_get_products(driver)

    products.sort_products("Price (low to high)")

    prices = [
        float(p.find_element(By.CLASS_NAME, "inventory_item_price").text.replace("$", ""))
        for p in driver.find_elements(By.CLASS_NAME, "inventory_item")
    ]

    assert prices == sorted(prices)


def test_sort_by_price_high_to_low(driver):
    products = login_and_get_products(driver)

    products.sort_products("Price (high to low)")

    prices = [
        float(p.find_element(By.CLASS_NAME, "inventory_item_price").text.replace("$", ""))
        for p in driver.find_elements(By.CLASS_NAME, "inventory_item")
    ]

    assert prices == sorted(prices, reverse=True)


def test_sort_by_name_az(driver):
    products = login_and_get_products(driver)

    products.sort_products("Name (A to Z)")

    names = [
        p.find_element(By.CLASS_NAME, "inventory_item_name").text
        for p in driver.find_elements(By.CLASS_NAME, "inventory_item")
    ]

    assert names == sorted(names)


def test_sort_by_name_za(driver):
    products = login_and_get_products(driver)

    products.sort_products("Name (Z to A)")

    names = [
        p.find_element(By.CLASS_NAME, "inventory_item_name").text
        for p in driver.find_elements(By.CLASS_NAME, "inventory_item")
    ]

    assert names == sorted(names, reverse=True)


def test_product_details(driver):
    products = login_and_get_products(driver)
    products.open_product_details(0)

    assert "inventory-item.html" in driver.current_url


def test_multiple_products_and_cart_counter(driver):
    products = login_and_get_products(driver)

    # Add product 0
    products.add_product_to_cart(0)
    assert products.get_cart_count() == 1

    # Add product 1
    products.add_product_to_cart(1)
    assert products.get_cart_count() == 2

    # Remove product 0
    products.remove_product_from_cart(0)
    assert products.get_cart_count() == 1
