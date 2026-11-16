from .base_page import BasePage
from .locators import ProductPageLocators


class ProductPage(BasePage):
    def get_product_name(self):
        return self.visible(ProductPageLocators.PRODUCT_NAME).text

    def get_product_price(self):
        return self.visible(ProductPageLocators.PRODUCT_PRICE).text

    def add_product_to_basket(self):
        self.click(ProductPageLocators.ADD_TO_BASKET)

    def should_be_added_product(self, expected_name):
        actual_name = self.visible(ProductPageLocators.ADDED_PRODUCT_NAME).text
        assert actual_name == expected_name, (
            f"Added product {actual_name!r} differs from {expected_name!r}"
        )

    def should_be_basket_total(self, expected_price):
        total = self.visible(ProductPageLocators.BASKET_TOTAL).text
        assert total == expected_price, (
            f"Basket total {total!r} differs from product price {expected_price!r}"
        )

    def should_not_be_success_message(self):
        assert self.is_not_element_present(*ProductPageLocators.SUCCESS_MESSAGE), (
            "Success message should not be present"
        )

    def wait_for_success_message(self):
        self.visible(ProductPageLocators.SUCCESS_MESSAGE)

    def should_disappear_success_message(self):
        self.visible(ProductPageLocators.SUCCESS_MESSAGE)
        assert self.is_disappeared(*ProductPageLocators.SUCCESS_MESSAGE), (
            "Success message did not disappear"
        )
