'''
Created on Feb 4, 2013

@author: nparoha
'''
import unittest

from selenium import webdriver

from edware_testing_automation.utils.preferences import preferences, Default

DOWNLOADS = preferences(Default.downloads_path)
UNZIPPED = preferences(Default.unzipped_path)


class EdTestBase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self._driver_name = preferences(Default.driver)

    def get_driver(self):
        firefoxProfile = webdriver.FirefoxProfile()
        #        firefoxProfile.native_events_enabled = True
        #        firefoxProfile.set_preference('webdriver_enable_native_events', True)
        firefoxProfile.set_preference('webdriver.enable.native.events', True)
        firefoxProfile.set_preference("browser.download.folderList", 2)
        firefoxProfile.set_preference("browser.download.manager.showWhenStarting", False)
        firefoxProfile.set_preference("browser.download.dir", DOWNLOADS)
        firefoxProfile.set_preference("browser.download.manager.scanWhenDone", False)
        firefoxProfile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                                      "text/csv, application/zip, application/octet-stream, application/csv, text/html;charset=utf-8")

        driver = webdriver.Firefox(firefoxProfile)

        if self._driver_name == 'chrome':
            driver = webdriver.ChromeOptions()
        driver.implicitly_wait(10)
        driver.maximize_window()
        return driver

    def get_url(self):
        return "http://{0}:{1}".format(preferences(Default.host), preferences(Default.port))

    def get_tsb_url(self):
        return "http://{0}:{1}".format(preferences(Default.tbs_host), preferences(Default.tbs_port))

    def get_hpz_url(self):
        return "http://{0}:{1}".format(preferences(Default.hpz_host), preferences(Default.hpz_port))
