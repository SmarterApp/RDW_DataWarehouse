__author__ = 'vnatarajan'

import time

from selenium.common.exceptions import NoSuchElementException

from edware_testing_automation.frontend_tests.filtering_helper import FilteringHelper


class PublicReportHelper(FilteringHelper):
    locators = {"hi": "class=hi_text",
                "help": "id=help",
                "globe_icon": "class=icon-globe",
                "download": "class=downloadIcon",
                "language": "class=selectedLanguage",
                }
    texts = {"language": "English"}

    def __init__(self, *args, **kwargs):
        FilteringHelper.__init__(self, *args, **kwargs)

    def component_check_in_page(self, math_alignment, ela_alignment):
        self.assertTrue(self.find_element(self.locators['globe_icon']), "Globe icon should present")
        self.assertTrue(self.find_element(self.locators['language']), "Language as English should present")
        element = self.find_element(self.locators['language'])
        self.assertEqual(element.text, self.texts['language'], "Language text is not correct")
        self.assertFalse(self.find_element(self.locators['hi']), "Hi text should not present")
        self.assertTrue(self.find_element(self.locators['help']).text == 'Info', "Help menu should not present")
        self.assertTrue(self.find_element(self.locators['download']), "Download option should present")
        self.check_cpop_legend_popup(False)
        self.check_alignment(math_alignment, ela_alignment)

        expected_grade_filters = ['Grade 3', 'Grade 4', 'Grade 5', 'Grade 6', 'Grade 7', 'Grade 8', 'Grade 11']
        filter_popup = self.open_filter_menu()
        self.check_grade_filter_menu(filter_popup, expected_grade_filters)
        self.select_grade_filter(filter_popup, ["Grade 6"])
        self.close_filter_menu(filter_popup, "apply")
        self.check_filter_bar(["Grades: 6"])
        time.sleep(7)
        expected_error_msg = 'There is no data available for your request.'
        self.assertEqual(expected_error_msg,
                         str(self.driver.find_element_by_id("content").find_element_by_id("errorMessage").text),
                         "Error message not found")
        # clear the filter selection
        self.driver.find_element_by_class_name('selectedFilterGroup').find_element_by_tag_name('a').click()

        # dowload popup checking
        self.check_download_popup()

    def check_download_popup(self):
        download_locators = {"downloadMenu": "id=DownloadMenuModal",
                             "download_header": "id=myModalLabel",
                             "download_text": "class=modal-body",
                             "download_button": "id=exportButton",
                             "download_description": "class=desc_block",
                             "note": "class=note"
                             }
        download_texts = {"download": "Download",
                          "download_description": "Download the current view as a CSV.",
                          "note": "Note: The downloads above will reflect any selections you have made, including academic year, assessment, and filters."
                          }
        download_popup = self.open_file_download_popup()
        self.check_export_options(download_popup, ['Current view'])
        self.assertEqual(self.get_element(download_locators['download_header']).text, download_texts['download'],
                         "Wrong header in download popup")
        text = self.driver.find_element_by_class_name("desc_block").text
        self.assertEqual(text, download_texts['download_description'], "Download description is not correct")
        self.assertEqual(self.get_element(download_locators['note']).text, download_texts['note'],
                         "Download note is not correct")
        self.assertEqual(self.get_element(download_locators['download_button']).text, download_texts['download'],
                         "Download button not present")
        self.close_file_download_popup(download_popup)

    def get_element(self, locator):
        element = self.find_element(locator)
        if element:
            return element
        else:
            return False

    def find_element(self, locator):
        locator_type, locator = locator.split('=')
        try:
            if locator_type == 'class':
                return self.driver.find_element_by_class_name(locator)
            elif locator_type == 'id':
                return self.driver.find_element_by_id(locator)
            else:
                self.assertRaises("Provide correct element type")
        except NoSuchElementException:
            return False
