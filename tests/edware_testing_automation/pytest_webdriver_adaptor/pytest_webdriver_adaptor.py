# -*- coding: utf-8 -*-
import allure
import pytest
from allure.constants import AttachmentType
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver


class Browser(WebDriver):
    def __init__(self):
        firefoxProfile = webdriver.FirefoxProfile()
        firefoxProfile.set_preference('webdriver.enable.native.events', True)
        firefoxProfile.set_preference("browser.download.folderList", 2)
        firefoxProfile.set_preference("browser.download.manager.showWhenStarting", False)
        firefoxProfile.set_preference("browser.download.dir", _test_settings.download_path)
        firefoxProfile.set_preference("browser.download.manager.scanWhenDone", False)
        firefoxProfile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                                      "text/csv, "
                                      "application/zip, "
                                      "application/octet-stream, "
                                      "application/csv, "
                                      "text/html;charset=utf-8"
                                      )
        super().__init__(firefoxProfile)
        self.maximize_window()
        self.implicitly_wait(10)


class _test_settings:
    pass


def browser():
    if not hasattr(_test_settings, "browser") or not _test_settings.browser:
        _test_settings.browser = Browser()
    return _test_settings.browser


def pytest_addoption(parser):
    group = parser.getgroup('webdriver-adaptor')
    group.addoption(
        '--always-last-screen',
        action='store_const',
        const='always_last_screen',
        default=False,
        help='If option is set, last browser\'s screen will be saved for passed tests.'
    )
    group.addoption(
        '--browser-download-path',
        action='store',
        dest='download_path',
        default='/tmp/downloads',
        help='Path for browser\'s downloads folder. Default: /tmp/downloads'
    )


def pytest_runtest_setup(item):
    _test_settings.download_path = item.config.option.download_path


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call':
        if (report.skipped or report.failed) or (
                    report.passed and item.config.option.always_last_screen):
            if getattr(_test_settings, "browser", None):
                url = _test_settings.browser.current_url
                if url is not None:
                    allure.attach('Latest URL', url, type=AttachmentType.TEXT)

                screen_shot = _test_settings.browser.get_screenshot_as_png()
                if screen_shot is not None:
                    allure.attach('Latest screen shot', screen_shot, type=AttachmentType.PNG)

                html = _test_settings.browser.page_source.encode('utf-8')
                if html is not None:
                    allure.attach('Latest HTML page', html, type=AttachmentType.HTML)
    return report


def pytest_runtest_teardown(item):
    if getattr(_test_settings, "browser", None):
        _test_settings.browser.quit()
        _test_settings.browser = None
