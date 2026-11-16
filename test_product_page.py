from uuid import uuid4

import pytest

from pages.basket_page import BasketPage
from pages.login_page import LoginPage
from pages.product_page import ProductPage


PRODUCT_LINK = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/"
LOGIN_LINK = "http://selenium1py.pythonanywhere.com/accounts/login/"


@pytest.mark.need_review
def test_guest_can_add_product_to_basket(browser):
    page = ProductPage(browser, PRODUCT_LINK)
    page.open()
    name, price = page.get_product_name(), page.get_product_price()
    page.add_product_to_basket()
    page.should_be_added_product(name)
    page.should_be_basket_total(price)


@pytest.mark.need_review
def test_guest_cant_see_product_in_basket_opened_from_product_page(browser):
    page = ProductPage(browser, PRODUCT_LINK)
    page.open()
    page.go_to_basket_page()
    basket = BasketPage(browser, browser.current_url)
    basket.should_be_empty_basket()
    basket.should_be_empty_basket_message()


@pytest.mark.need_review
def test_guest_can_go_to_login_page_from_product_page(browser):
    page = ProductPage(browser, PRODUCT_LINK)
    page.open()
    page.go_to_login_page()
    LoginPage(browser, browser.current_url).should_be_login_page()


@pytest.mark.add_to_basket
class TestUserAddToBasketFromProductPage:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        page = LoginPage(browser, LOGIN_LINK)
        page.open()
        page.register_new_user(f"autotest-{uuid4().hex}@example.com", "Test-Password-42!")

    @pytest.mark.need_review
    def test_user_can_add_product_to_basket(self, browser):
        page = ProductPage(browser, PRODUCT_LINK)
        page.open()
        name, price = page.get_product_name(), page.get_product_price()
        page.add_product_to_basket()
        page.should_be_added_product(name)
        page.should_be_basket_total(price)


@pytest.mark.promo
@pytest.mark.parametrize("link", [
    pytest.param(
        f"{PRODUCT_LINK}?promo=offer{i}",
        marks=pytest.mark.xfail(
            reason="offer7 changes the product name in the success message", strict=True,
        ) if i == 7 else (),
        id=f"offer{i}",
    )
    for i in range(10)
])
def test_guest_can_add_product_to_basket_with_promo(browser, link):
    page = ProductPage(browser, link)
    page.open()
    name, price = page.get_product_name(), page.get_product_price()
    page.add_product_to_basket()
    page.solve_quiz_and_get_code()
    page.should_be_added_product(name)
    page.should_be_basket_total(price)


def test_guest_cant_see_success_message(browser):
    page = ProductPage(browser, PRODUCT_LINK)
    page.open()
    page.should_not_be_success_message()


@pytest.mark.xfail(reason="Adding a product displays a success message", strict=True)
def test_guest_cant_see_success_message_after_adding_product_to_basket(browser):
    page = ProductPage(browser, PRODUCT_LINK)
    page.open()
    page.add_product_to_basket()
    page.wait_for_success_message()
    page.should_not_be_success_message()


@pytest.mark.xfail(reason="Success message does not disappear automatically", strict=True)
def test_message_disappeared_after_adding_product_to_basket(browser):
    page = ProductPage(browser, PRODUCT_LINK)
    page.open()
    page.add_product_to_basket()
    page.should_disappear_success_message()
