from behave import fixture, use_fixture
from selenium import webdriver
import os
import smtplib
import imghdr
from email.message import EmailMessage

MY_PORT = 587
HOST_ADDRESS = "smtp.yandex.ru"
FROM_ADDRESS = "BlackKnightGreatsword@yandex.ru"
TO_ADDRESS = "BlackKnightGreataxe@yandex.ru"


@fixture
def browser_firefox(context):
    # login into mail
    smtp_server = smtplib.SMTP(host=HOST_ADDRESS, port=MY_PORT)
    smtp_server.starttls()
    smtp_server.login(FROM_ADDRESS, input("Password: "))
    # start webdriver
    context.browser = webdriver.Firefox()
    context.screenshots = []
    context.timeout = 10
    context.browser.maximize_window()
    yield context.browser
    # after finishing scenario
    # send mail
    msg = EmailMessage()
    msg['From'] = FROM_ADDRESS
    msg['To'] = TO_ADDRESS
    msg['Subject'] = "test screenshots"
    for file in context.screenshots:
        with open(file, 'rb') as fp:
            img_data = fp.read()
        msg.add_attachment(img_data, maintype='image', subtype=imghdr.what(None, img_data))
    smtp_server.send_message(msg)
    # cleanup
    for file in context.screenshots:
        os.remove(file)
    smtp_server.quit()
    context.browser.quit()


def before_all(context):
    use_fixture(browser_firefox, context)
