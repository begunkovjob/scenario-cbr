from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains


class BasePage:
    def __init__(self, context):
        self.browser = context.browser
        self.timeout = context.timeout

    locators = {}

    def find_element(self, *loc):
        return self.browser.find_element(*loc)

    def assert_element(self, element_name):
        assert WebDriverWait(self.browser, self.timeout).until(
            ec.presence_of_element_located(self.locators[element_name]))

    def move_to_element(self, element_name):
        element = WebDriverWait(self.browser, self.timeout).until(
            ec.visibility_of_element_located(self.locators[element_name]))
        actions = ActionChains(self.browser)
        actions.move_to_element(element).perform()

    def get_element_text(self, element_name):
        element = WebDriverWait(self.browser, self.timeout).until(
            ec.visibility_of_element_located(self.locators[element_name]))
        return element.text

    def send_keys_to_element(self, element_name, keys):
        self.move_to_element(element_name)
        WebDriverWait(self.browser, self.timeout).until(
            ec.visibility_of_element_located(self.locators[element_name])).send_keys(keys)

    def click_element(self, element_name):
        self.move_to_element(element_name)
        WebDriverWait(self.browser, self.timeout).until(
            ec.element_to_be_clickable(self.locators[element_name])).click()


class Google(BasePage):
    """https://www.google.ru"""
    locators = {
        "search_field": (By.NAME, "q"),
        "submit": (By.NAME, "btnK")
    }


class Cbr(BasePage):
    """https://www.cbr.ru"""
    locators = {
        "reception": (By.XPATH, "//*[@href='/Reception/']"),
        "menu": (By.XPATH, "//span[@class='burger']")
    }


class CbrReception(BasePage):
    """https://www.cbr.ru/Reception/"""
    locators = {
        "gratitude": (By.XPATH, "//*[@href='/Reception/Message/Register?messageType=Gratitude']")
    }


class CbrReceptionGratitude(BasePage):
    """https://www.cbr.ru/Reception/Message/Register?messageType=Gratitude"""
    locators = {
        "message_body": (By.ID, "MessageBody"),
        "agreement_flag": (By.ID, "_agreementFlag")
    }


class CbrMenu(BasePage):
    """https://www.cbr.ru"""
    locators = {
        "about": (By.XPATH, "//*[@class='pseudo'][@href='/About/']")
    }


class CbrAbout(BasePage):
    """https://www.cbr.ru"""
    locators = {
        "about_warning": (By.XPATH, "//*[@href='/About/warning/']")
    }


class CbrAboutWarning(BasePage):
    """https://www.cbr.ru/About/warning/"""
    locators = {
        "content": (By.ID, "content"),
        "switch_en": (By.XPATH, "//*[contains(@href, 'to=en-GB')]")
    }


class CbrAboutWarningEn(BasePage):
    """https://www.cbr.ru/eng/About/warning/"""
    locators = {
        "content": (By.ID, "content")
    }
