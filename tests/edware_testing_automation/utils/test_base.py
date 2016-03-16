'''
Created on Feb 4, 2013

@author: nparoha
'''
import unittest

import allure
from allure.constants import AttachmentType
from selenium.webdriver.support.wait import WebDriverWait

from edware_testing_automation.pytest_webdriver_adaptor.pytest_webdriver_adaptor import browser
from edware_testing_automation.utils.preferences import preferences, Default

DOWNLOADS = preferences(Default.downloads_path)
UNZIPPED = preferences(Default.unzipped_path)


def add_screen_to_report(name):
    allure.attach(name, browser().get_screenshot_as_png(), type=AttachmentType.PNG)


def wait_for(method, seconds=60, message=''):
    return WebDriverWait(browser(), seconds).until(method, message)


class EdTestBase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

    def get_url(self):
        return "http://{0}:{1}".format(preferences(Default.host), preferences(Default.port))

    def get_tsb_url(self):
        return "http://{0}:{1}".format(preferences(Default.tbs_host), preferences(Default.tbs_port))

    def get_hpz_url(self):
        return "http://{0}:{1}".format(preferences(Default.hpz_host), preferences(Default.hpz_port))
