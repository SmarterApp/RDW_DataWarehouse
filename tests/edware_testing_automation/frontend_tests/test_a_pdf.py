'''
Created on May 20, 2013

@author: nparoha
'''
import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from edware_testing_automation.frontend_tests.common_session_share_steps import SessionShareHelper
from edware_testing_automation.pytest_webdriver_adaptor.pytest_webdriver_adaptor import browser
from edware_testing_automation.utils.preferences import preferences, Edware
from edware_testing_automation.utils.test_base import add_screen_to_report, wait_for

_pdfs = preferences(Edware.report_dir)


# @attr('pdf')
class PdfTest(SessionShareHelper):
    def __init__(self, *args, **kwargs):
        SessionShareHelper.__init__(self, *args, **kwargs)

    ''' setUp: Open webpage '''

    def setUp(self):
        self.open_requested_page_redirects_login_page("state_view_sds")
        self.enter_login_credentials("shall", "shall1234")
        self.check_redirected_requested_page("state_view_sds")

    def test_color_pdf(self):
        print("TC_COLOR_PDF: Validate that the pdf is printed from the UI and a directory structure is available.")
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("242", "ui-jqgrid-ftable")
        self.drill_down_navigation("03", "jqgfirstrow")
        add_screen_to_report('/tmp/test_color_pdf.png')
        # Click on 'Lettie L Hose' student link from list of students
        self.drill_down_navigation("jqg26", "overallScoreSection")

        print("PDF: Click on the print button to generate a pdf.")
        browser().find_element_by_class_name("printLabel").click()
        wait_for(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "modal-backdrop")))
        print_popup = browser().find_element_by_id("PrintModal")
        self.check_print_popover_contents(print_popup, "color")
        time.sleep(20)
        print("PDF: Validate if the directory structure is available.")
        assert os.path.isdir(_pdfs + "/NC/2016/228/242/03/isr/SUMMATIVE")

        print("PDF: Validate if the pdf file is stored inside the directory structure.")
        assert os.path.isfile(
            _pdfs + "/NC/2016/228/242/03/isr/SUMMATIVE/dae1acf4-afb0-4013-90ba-9dcde4b25621.20160410.en.pdf")
        print("PDF: Color pdf tests passed.")

    def test_grayscale_pdf(self):
        print("TC_GRAYSCALE_PDF: Validate that the pdf is printed from the UI and a directory structure is available.")
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("242", "ui-jqgrid-ftable")
        self.drill_down_navigation("03", "jqgfirstrow")
        self.drill_down_navigation("jqg26", "overallScoreSection")

        print("PDF: Click on the print button to generate a pdf.")
        browser().find_element_by_class_name("printLabel").click()
        wait_for(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "modal-backdrop")))
        print("PDF: Verify the contents of the pdf popover and generate a grayscale pdf printout")
        print_popup = browser().find_element_by_id("PrintModal")
        self.check_print_popover_contents(print_popup, "grayscale")
        time.sleep(20)
        print("PDF: Validate if the directory structure is available.")
        assert (os.path.isdir(_pdfs + "/NC/2016/228/242/03/isr/SUMMATIVE"))

        print("PDF: Validate if the pdf file is stored inside the directory structure.")
        assert os.path.isfile(
            _pdfs + "/NC/2016/228/242/03/isr/SUMMATIVE/dae1acf4-afb0-4013-90ba-9dcde4b25621.20160410.en.g.pdf")
        print("PDF: Grayscale pdf tests passed.")

    def check_print_popover_contents(self, print_popover, pdf_type):
        self.assertEqual(str(print_popover.find_element_by_id("myModalLabel").get_attribute("innerHTML")), "Print",
                         "Pdf print popup header incorrectly displayed")
        print_option = print_popover.find_element_by_class_name("modal-body").find_elements_by_tag_name("input")
        wait_for(expected_conditions.element_to_be_clickable(
            (By.XPATH, "//div[@id='PrintModal']//input[@name='print']")))
        wait_for(expected_conditions.element_to_be_clickable((By.XPATH, "//div[@id='PrintModal']//button")))
        option = None
        if pdf_type == "grayscale":
            option = print_option[0]
        elif pdf_type == "color":
            option = print_option[1]
        else:
            print("incorrect pdf color specified")
        option.click()
        add_screen_to_report('/tmp/pdf_debug.png')
        print_button = print_popover.find_element_by_class_name("modal-footer").find_element_by_class_name("btn")
        print_button.click()
