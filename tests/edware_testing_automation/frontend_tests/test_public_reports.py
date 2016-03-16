from edware_testing_automation.frontend_tests.public_report_helper import PublicReportHelper
from edware_testing_automation.pytest_webdriver_adaptor.pytest_webdriver_adaptor import browser


class PublicReports(PublicReportHelper):
    elements = {"Find": "id=SearchBoxTemplate"}

    def __init__(self, *args, **kwargs):
        PublicReportHelper.__init__(self, *args, **kwargs)

    ''' setUp: Open webpage '''

    def setUp(self):
        self.open_requested_page_redirects_login_page("state_view_sds_public_report")
        self.check_redirected_requested_page("state_view_sds_public_report")

    def test_public_report_sunset_no_access_to_grade_view(self):
        self.check_breadcrumb_hierarchy_links(["North Carolina"])
        self.component_check_in_page(["50%", "50%"], ["60%", "40%"])
        self.assertTrue(self.find_element(self.elements['Find']), "Find text box should present")
        district = "Sunset School District"
        self._click_by_text(district)
        self.check_breadcrumb_trail(district)
        self.component_check_in_page(["45%", "55%"], ["62%", "38%"])
        self.assertTrue(self.find_element(self.elements['Find']), "Find text box should present")
        school = "Sunset - Eastern Elementary"
        self._click_by_text(school)
        self.check_breadcrumb_trail(school)
        self.component_check_in_page(["48%", "52%"], ["69%", "31%"])
        self.assertFalse(self.find_element(self.elements['Find']), "Find text box should present")
        self.check_pr_grade_acess("03")

    def _click_by_text(self, text):
        browser().find_element_by_xpath("//a[contains(text(), '{text}')]".format(text=text)).click()
