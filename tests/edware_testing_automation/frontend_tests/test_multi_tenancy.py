"""
Created on Feb 4, 2014

@author: nparoha
"""
import allure

from edware_testing_automation.frontend_tests.comparing_populations_helper import ComparingPopulationsHelper
from edware_testing_automation.pytest_webdriver_adaptor.pytest_webdriver_adaptor import browser


@allure.feature(
    'Smarter: State view',
    'Smarter: District view',
    'Smarter: School view',
    'Smarter: Grade view'
)
@allure.story('Legend & info')
class MultiTenancy(ComparingPopulationsHelper):
    """
    Tests for Multi Tenancy to ensure that user sees information for their tenants only
    """

    def __init__(self, *args, **kwargs):
        ComparingPopulationsHelper.__init__(self, *args, **kwargs)

    def test_ca_tenant_login(self):
        self.open_landing_page_login_page()
        self.enter_login_credentials("msollars", "msollars1234")
        self.check_redirected_requested_page("state_view_ca_tenant")

        self.assertEqual("California", str(
            browser().find_element_by_id("breadcrumb").text)), "Breadcrumb for state 'North Carolina' not found"
        self.check_headers("Matt Sollars", "Log Out")
        self.check_page_header("Districts in California")
        self.check_tenant_logo('smarterHeader_logo')
        # Click on 'Dealfish Pademelon SD' link from list of districts
        self.drill_down_navigation("2ce72d77-1de2-4137-a083-77935831b817", "ui-jqgrid-ftable")
        # Click on 'Dolphin Razorfish Sch' school link from list of schools
        self.drill_down_navigation("0eab62f5-6c97-4302-abff-7bfdc61f527c", "ui-jqgrid-ftable")
        self.select_academic_year("2015")
        # Click on 'Grade 3' school link from list of grades
        self.drill_down_navigation("03", "jqgfirstrow")
        # Click on 'Nelson, Warren ' student link from list of students
        self.drill_down_navigation("jqg24", "overallScoreSection")
        breadcrumb_list = ["California", "Dealfish Pademelon SD", "Dolphin Razorfish Sch", "Grade 03"]
        self.check_breadcrumb_hierarchy_links(breadcrumb_list)

    def test_nc_tenant_login(self):
        self.open_landing_page_login_page()
        self.enter_login_credentials("vlee", "vlee1234")
        self.check_redirected_requested_page("state_view_sds")
        self.assertEqual("North Carolina", str(
            browser().find_element_by_id("breadcrumb").text)), "Breadcrumb for state 'North Carolina' not found"
        self.check_headers("Victor Lee", "Log Out")
        self.check_page_header("Districts in North Carolina")
        self.check_tenant_logo('NC')
        self.check_tenant_label("North Carolina Reporting")
        # Click on 'Sunset School District' link from list of districts
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        # Click on 'Sunset - Eastern Elementary' school link from list of schools
        self.drill_down_navigation("242", "ui-jqgrid-ftable")
        # Click on 'Grade 3' school link from list of grades
        self.drill_down_navigation("03", "jqgfirstrow")
        # Click on 'Lettie L Hose' student link from list of students
        self.drill_down_navigation("jqg26", "overallScoreSection")

        print("TC_breadcrumbs: Validate the active links and current view in the breadcrumb trail")
        breadcrumb_list = ["North Carolina", "Sunset School District", "Sunset - Eastern Elementary", "Grade 03"]
        self.check_breadcrumb_hierarchy_links(breadcrumb_list)
