from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import os
import uuid

from pages import Google, Cbr, CbrReception, CbrReceptionGratitude, CbrMenu, CbrAbout, \
    CbrAboutWarning, CbrAboutWarningEn


@given("website '{url}'")
def step(context, url):
    context.browser.get(url)


@then("check google search field exists")
def step(context):
    page = Google(context)
    page.assert_element("search_field")


@when("enter google query '{query}'")
def step(context, query):
    page = Google(context)
    page.send_keys_to_element("search_field", query)


@when("click google submit")
def step(context):
    page = Google(context)
    page.click_element("submit")


@then("check link exists '{url}'")
def step(context, url):
    assert WebDriverWait(context.browser, context.timeout).until(
        ec.presence_of_element_located((By.PARTIAL_LINK_TEXT, url)))


@when("click link '{url}'")
def step(context, url):
    element = WebDriverWait(context.browser, context.timeout).until(
        ec.presence_of_element_located((By.PARTIAL_LINK_TEXT, url)))
    href = element.get_attribute("href")
    number_of_windows = len(context.browser.window_handles)
    element.click()
    # wait until new tab opens
    WebDriverWait(context.browser, context.timeout).until(
        ec.number_of_windows_to_be(number_of_windows + 1))
    # find window with newly opened link and switch to it
    found = False
    for window in context.browser.window_handles:
        context.browser.switch_to.window(window)
        if context.browser.current_url.find(href) == 0:
            found = True
    if not found:
        Exception("Window not found")


@then("check url '{url}'")
def step(context, url):
    assert WebDriverWait(context.browser, context.timeout).until(ec.url_contains(url))


@when("click reception")
def step(context):
    page = Cbr(context)
    page.click_element("reception")


@when("click gratitude")
def step(context):
    page = CbrReception(context)
    page.click_element("gratitude")


@when("enter message '{text}'")
def step(context, text):
    page = CbrReceptionGratitude(context)
    page.send_keys_to_element("message_body", text)


@when("checkbox agree")
def step(context):
    page = CbrReceptionGratitude(context)
    page.click_element("agreement_flag")


@then("take screenshot")
def step(context):
    # find or create screenshots dir
    screenshot_path = os.path.join(os.path.abspath(os.getcwd()), "screenshots")
    if not os.path.exists(screenshot_path):
        os.mkdir(screenshot_path)
    if not os.path.isdir(screenshot_path):
        Exception("Path to screenshots dir does not exist and cannot be created")
    # generate unique filename and save screenshot
    filename = os.path.join(screenshot_path, f"{uuid.uuid4()}.png")
    context.screenshots.append(filename)
    context.browser.save_screenshot(filename)


@when("click menu")
def step(context):
    page = Cbr(context)
    page.click_element("menu")


@when("click about")
def step(context):
    page = CbrMenu(context)
    page.click_element("about")


@when("click warning")
def step(context):
    page = CbrAbout(context)
    page.click_element("about_warning")


@then("save warning")
def step(context):
    page = CbrAboutWarning(context)
    context.warning_text = page.get_element_text("content")


@when("switch language to en")
def step(context):
    page = CbrAboutWarning(context)
    page.click_element("switch_en")


@then("compare warning text")
def step(context):
    page = CbrAboutWarningEn(context)
    assert context.warning_text != page.get_element_text("content")
