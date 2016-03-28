'''
Created on Aug 13, 2013

@author: nparoha
'''

from edware_testing_automation.frontend_tests.comparing_populations_helper import ComparingPopulationsHelper
from edware_testing_automation.frontend_tests.filtering_helper import FilteringHelper


class TestE2E(FilteringHelper, ComparingPopulationsHelper):
    def __init__(self, *args, **kwargs):
        FilteringHelper.__init__(self, *args, **kwargs)
        ComparingPopulationsHelper.__init__(self, *args, **kwargs)

    def test_e2e_frontend_one_assmt_flow1(self):
        self.open_requested_page_redirects_login_page("state_view_sds")

        ''' Invalid Login Credentials tests are disabled for DE126'''
        #        ## Invalid login credentials
        #        login_page = browser().find_element_by_class_name("box-content")
        #        login_page.find_element_by_id("IDToken1").send_keys("shall")
        #        login_page.find_element_by_id("IDToken2").send_keys("1234")
        #        login_page.find_element_by_name("Login.Submit").click()
        #        incorrect_login_msg = browser().find_element_by_class_name("clear-float").text
        #        expected_msg = "Invalid username/password combination. Please re-enter your credentials."
        #        self.assertIn(expected_msg, incorrect_login_msg), "Invalid user/password redirect page displaying incorrect text"
        #        browser().find_element_by_partial_link_text("Return to login page").click()

        ## Login as a Teacher
        self.enter_login_credentials("shall", "shall1234")
        self.check_redirected_requested_page("state_view_sds")
        # Turn the Alignment option ON. Validate the functionality and turn it off.
        self.check_alignment(["50%", "50%"], ["60%", "40%"])
        ## Check default sort order in the grid
        self.check_topmost_row("Daybreak School District")

        ## Validate the sorting functionality
        self.sort_by_asmt("ela", "Dealfish Pademelon SD", "ELA (proficiency: least to most)")
        self.sort_by_asmt("Math", "Daybreak School District", "Math (proficiency: least to most)")

# ## Turn Alignment option ON and test few different sort options
#        browser().find_element_by_class_name("align_button").click()
#        self.check_bars_aligned()
#        self.select_sort_option("math", 2, "desc", "Sunset School District")
#        self.check_bars_aligned()
#        self.sort_by_entity_name("Daybreak School District")
#        self.check_bars_aligned()
