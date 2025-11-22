
import pytest
from pages.login_page import LoginPage
from test_data import users  # ← نستورد البيانات

@pytest.mark.parametrize("user_data", users, ids=[user["description"] for user in users])
def test_login_behavior(driver, user_data):
    """
    اختبار تسجيل الدخول مع بيانات مختلفة
    """
    login_page = LoginPage(driver)

    # نستخدم بيانات المستخدم من parametrize
    username = user_data["username"]
    password = user_data["password"]
    expected_behavior = user_data["expected_behavior"]

    # نحاول تسجيل الدخول
    login_page.login(username, password)

    # نشوف النتيجة بناءً على نوع المستخدم
    if expected_behavior == "normal":
        # المستخدم العادي لازم يدخل
        assert login_page.is_logged_in(), f"Expected login to succeed for {username}"
    elif expected_behavior == "locked_out":
        # المستخدم المغلق لازم يظهرله رسالة
        assert login_page.is_locked_out_error(), f"Expected locked out error for {username}"
    elif expected_behavior == "problematic_images":
        # نشوف مثلاً هل الصور ظاهرة صح؟
        assert login_page.has_broken_images() == True, f"Images should be broken for {username}"
    elif expected_behavior == "slow":
        # نشوف مثلاً هل الصفحة فتحت ببطء؟ (ممكن نقيس الوقت)
        assert login_page.is_page_loaded_quickly() == True, f"Page should load quickly for {username}"