# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

"""
Created on Feb 4, 2013

@author: nparoha
"""
import unittest

import allure
from allure.constants import AttachmentType
from selenium.webdriver.support.wait import WebDriverWait

from edware_testing_automation.pytest_webdriver_adaptor.pytest_webdriver_adaptor import browser
from edware_testing_automation.utils.preferences import preferences, Default

DOWNLOADS = preferences(Default.downloads_path)
UNZIPPED = preferences(Default.unzipped_path)


def save_screen(name):
    allure.attach(name, browser().get_screenshot_as_png(), type=AttachmentType.PNG)


def save_message(message, name='Additional information'):
    allure.attach(name, message, type=AttachmentType.TEXT)


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
