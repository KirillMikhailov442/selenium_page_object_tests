from urllib.parse import urlparse

from .base_page import BasePage
from .locators import LoginPageLocators


class LoginPage(BasePage):
    def should_be_login_page(self):
        self.should_be_login_url()
        self.should_be_login_form()
        self.should_be_register_form()

    def should_be_login_url(self):
        assert "/accounts/login" in urlparse(self.browser.current_url).path, (
            f"Expected login page, got {self.browser.current_url}"
        )

    def should_be_login_form(self):
        assert self.is_element_present(*LoginPageLocators.LOGIN_FORM), "Login form is absent"

    def should_be_register_form(self):
        assert self.is_element_present(*LoginPageLocators.REGISTER_FORM), "Registration form is absent"

    def register_new_user(self, email, password):
        self.visible(LoginPageLocators.EMAIL).send_keys(email)
        self.visible(LoginPageLocators.PASSWORD).send_keys(password)
        self.visible(LoginPageLocators.CONFIRM_PASSWORD).send_keys(password)
        self.click(LoginPageLocators.REGISTER_BUTTON)
        self.should_be_authorized_user()
