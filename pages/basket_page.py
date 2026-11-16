from .base_page import BasePage
from .locators import BasketPageLocators


class BasketPage(BasePage):
    def should_be_empty_basket(self):
        assert self.is_not_element_present(*BasketPageLocators.BASKET_ITEMS), (
            "Basket contains unexpected products"
        )

    def should_be_empty_basket_message(self):
        message = self.visible(BasketPageLocators.EMPTY_BASKET_MESSAGE).text
        assert "Your basket is empty" in message, f"Unexpected empty basket message: {message!r}"
