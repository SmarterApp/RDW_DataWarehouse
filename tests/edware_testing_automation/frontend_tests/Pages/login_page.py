__author__ = 'vnatarajan'

# from functional_tests.utils.py.base.py import SbacBaseClass
# from functional_tests.utils.py.utils.py import WebDriver
# from functional_tests.utils.py.base import SbacBaseClass

from selenium.webdriver.common.by import By

# locators = {
#     'username': 'id=IDToken1',
#     'password': 'id=IDToken2',
#     'submit': 'name=Login.Submit',
#     'forgotpassword': 'tag=a'
# }

username = (By.ID, 'IDToken1')
password = (By.ID, 'IDToken2')
submitButton = (By.NAME, 'Login.Submit')


class LoginPage():
    timeout_seconds = 20

    def __init__(self, driver):
        self.driver = driver

    # def find_element_by_locator(self, locator):
    #     self.driver.find_element_by_locator(locator)

    def set_usrname(self, username):
        usernameElement = self.driver.find_element(*LoginPage.username)
        usernameElement.send_keys(username)

    def set_password(self, password):
        passwordElement = self.driver.find_element(*LoginPage.password)
        passwordElement.send_keys(password)

    def submit(self):
        submitButtonElement = self.driver.find_element(*LoginPage.submitButton)
        submitButtonElement.click()

    def login(self, username, password):
        self.set_usrname(username)
        self.set_password(password)
        self.submit()
