import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from selenium.webdriver.common.by import By


@pytest.mark.parametrize("driver", ["firefox"], indirect=True)
def test_multiple_products_checkout(driver):
    """
    Test checkout flow with multiple products
    """
    # 🔐 Login
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    products = ProductsPage(driver)
    products.wait_for_page_to_load()

    # 🛒 Add multiple products to cart
    product_indices = [0, 2, 4]  # هنضيف 3 منتجات مختلفة
    selected_products = []

    for index in product_indices:
        product_name = products.get_product_name(index)
        selected_products.append(product_name)
        products.add_product_to_cart(index)
        print(f"✅ Added product: {product_name}")

    # ✅ Verify cart badge count
    cart_count = products.get_cart_count()
    assert cart_count == len(product_indices), f"Expected {len(product_indices)} items in cart, got {cart_count}"
    print(f"✅ Cart badge shows: {cart_count} items")

    # 🛒 Go to cart
    products.go_to_cart()

    cart = CartPage(driver)
    cart.wait_for_cart_to_load()

    # ✅ Verify all products are in cart
    cart_items_count = cart.get_items_count()
    assert cart_items_count == len(product_indices), f"Expected {len(product_indices)} items, got {cart_items_count}"
    print(f"✅ Cart contains {cart_items_count} items")

    # ✅ Verify product names in cart
    cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
    cart_product_names = [
        item.find_element(By.CLASS_NAME, "inventory_item_name").text
        for item in cart_items
    ]

    for product_name in selected_products:
        assert product_name in cart_product_names, f"Product '{product_name}' not found in cart!"
        print(f"✅ Product '{product_name}' found in cart")

    # 💰 Get product prices from cart
    cart_prices = []
    for item in cart_items:
        price_text = item.find_element(By.CLASS_NAME, "inventory_item_price").text
        # Remove '$' and convert to float
        price = float(price_text.replace("$", ""))
        cart_prices.append(price)
        print(f"   Price: ${price}")

    expected_subtotal = sum(cart_prices)
    print(f"✅ Expected subtotal: ${expected_subtotal:.2f}")

    # 🧾 Proceed to checkout
    cart.click_checkout()

    checkout = CheckoutPage(driver)

    # 📝 Fill checkout information
    checkout.fill_checkout_info("Ibrahim", "Mohamed", "12345")
    checkout.click_continue()

    # ✅ Verify we're on step-two
    assert "checkout-step-two" in driver.current_url, f"Not on checkout-step-two! Current: {driver.current_url}"
    print("✅ Reached checkout-step-two")

    # 💵 Verify items on checkout overview page
    overview_items = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(overview_items) == len(product_indices), f"Expected {len(product_indices)} items on overview"
    print(f"✅ Overview shows {len(overview_items)} items")

    # 💰 Verify prices on overview
    overview_prices = []
    for item in overview_items:
        price_text = item.find_element(By.CLASS_NAME, "inventory_item_price").text
        price = float(price_text.replace("$", ""))
        overview_prices.append(price)

    assert overview_prices == cart_prices, "Prices mismatch between cart and overview!"
    print("✅ All prices match between cart and overview")

    # 🧮 Verify subtotal calculation
    subtotal_text = driver.find_element(By.CLASS_NAME, "summary_subtotal_label").text
    # Extract number from "Item total: $XX.XX"
    subtotal_value = float(subtotal_text.split("$")[1])
    assert subtotal_value == expected_subtotal, f"Subtotal mismatch! Expected ${expected_subtotal:.2f}, got ${subtotal_value:.2f}"
    print(f"✅ Subtotal verified: ${subtotal_value:.2f}")

    # 💸 Verify tax
    tax_text = driver.find_element(By.CLASS_NAME, "summary_tax_label").text
    tax_value = float(tax_text.split("$")[1])
    print(f"✅ Tax: ${tax_value:.2f}")

    # 💳 Verify total
    total_text = driver.find_element(By.CLASS_NAME, "summary_total_label").text
    total_value = float(total_text.split("$")[1])
    expected_total = subtotal_value + tax_value
    assert total_value == expected_total, f"Total mismatch! Expected ${expected_total:.2f}, got ${total_value:.2f}"
    print(f"✅ Total verified: ${total_value:.2f} (${subtotal_value:.2f} + ${tax_value:.2f})")

    # ✅ Complete the order
    checkout.click_finish()

    # 🎉 Verify checkout complete
    assert checkout.is_checkout_complete(), "Checkout not completed!"

    complete_text = driver.find_element(By.CLASS_NAME, "complete-header").text
    assert complete_text == "Thank you for your order!", f"Unexpected completion message: {complete_text}"

    assert "checkout-complete" in driver.current_url, "Not on checkout-complete page!"

    print("🎉 ✅ Multiple products checkout completed successfully!")