import math

from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .locators import BasePageLocators


class BasePage:
    def __init__(self, browser, url, timeout=10):
        self.browser = browser
        self.url = url
        self.timeout = timeout

    def open(self):
        self.browser.get(self.url)

    def visible(self, locator):
        return WebDriverWait(self.browser, self.timeout).until(
            EC.visibility_of_element_located(locator),
            message=f"Element should be visible: {locator}",
        )

    def click(self, locator):
        WebDriverWait(self.browser, self.timeout).until(
            EC.element_to_be_clickable(locator),
            message=f"Element should be clickable: {locator}",
        ).click()

    def is_element_present(self, how, what):
        try:
            WebDriverWait(self.browser, self.timeout).until(
                EC.presence_of_element_located((how, what))
            )
        except TimeoutException:
            return False
        return True

    def is_not_element_present(self, how, what, timeout=4):
        try:
            WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located((how, what))
            )
        except TimeoutException:
            return True
        return False

    def is_disappeared(self, how, what, timeout=4):
        try:
            WebDriverWait(self.browser, timeout, poll_frequency=1).until_not(
                EC.presence_of_element_located((how, what))
            )
        except TimeoutException:
            return False
        return True

    def go_to_login_page(self):
        self.click(BasePageLocators.LOGIN_LINK)

    def should_be_login_link(self):
        assert self.is_element_present(*BasePageLocators.LOGIN_LINK), "Login link is absent"

    def go_to_basket_page(self):
        self.click(BasePageLocators.BASKET_LINK)

    def should_be_authorized_user(self):
        assert self.is_element_present(*BasePageLocators.USER_ICON), "User is not authorized"

    def solve_quiz_and_get_code(self):
        alert = WebDriverWait(self.browser, self.timeout).until(EC.alert_is_present())
        x = alert.text.split(" ")[2]
        alert.send_keys(str(math.log(abs(12 * math.sin(float(x))))))
        alert.accept()
        try:
            alert = self.browser.switch_to.alert
            print(f"Your code: {alert.text}")
            alert.accept()
        except NoAlertPresentException:
            pass
