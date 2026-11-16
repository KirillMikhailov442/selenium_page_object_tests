import pytest
from selenium import webdriver


def pytest_addoption(parser):
    parser.addoption("--language", action="store", default="en",
                     help="Preferred browser language, for example en, es or fr")
    parser.addoption("--browser_name", action="store", default="chrome",
                     choices=("chrome", "firefox"))
    parser.addoption("--headless", action="store_true", default=False)


@pytest.fixture
def browser(request):
    language = request.config.getoption("--language")
    if request.config.getoption("--browser_name") == "firefox":
        options = webdriver.FirefoxOptions()
        options.set_preference("intl.accept_languages", language)
        if request.config.getoption("--headless"):
            options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
    else:
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"intl.accept_languages": language})
        if request.config.getoption("--headless"):
            options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
    driver.set_window_size(1440, 1000)
    driver.set_page_load_timeout(45)
    yield driver
    driver.quit()
