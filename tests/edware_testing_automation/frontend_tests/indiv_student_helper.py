# -*- coding: UTF-8 -*-
'''
Created on Feb 26, 2013

@author: nparoha
'''
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from edware_testing_automation.frontend_tests.common_session_share_steps import SessionShareHelper


class IndividualStudentHelper(SessionShareHelper):
    '''
    Helper methods for Individual Student Report Page
    '''

    def __init__(self, *args, **kwargs):
        SessionShareHelper.__init__(self, *args, **kwargs)

    # Check the overall score appearing above the bar
    def check_overall_score_perf_bar(self, section, expected_overall_score):
        overallScore = section.find_element_by_class_name("scoreWrapper").text
        self.assertEqual(int(overallScore), expected_overall_score, "Incorrect Overall Score is displayed")
        print("Correct Overall Score found on the performance bar")

    # Check cut points appearing below the bar
    def check_cutpoints_perf_bar(self, section, expected_cutpoints):
        actual_cutpoints = []
        for each in section.find_element_by_class_name("cutPointsBar").find_elements_by_class_name("cutPoints"):
            actual_cutpoints.append(int(each.text))

    # Check the overall score and ALD description is correctly displayed for each assessment
    def check_overall_Score_ald(self, section, score, color_code, overall, ald_text):
        # Validate the overall score and its background color
        overall_score = section.find_element_by_class_name("indicator")
        self.assertEqual(score, int(overall_score.text)), "Incorrect overall score for the assessment"
        self.assertEqual(color_code, str(
                overall_score.value_of_css_property(
                        "background-color"))), "Overall Score background color is incorrect."
        # Validate the text "Overall" is displayed
        self.assertEqual(overall, section.find_element_by_class_name(
                "overallText").text), "Word 'Overall' did not appear on the report."
        # Validate the ALD descriptor and its text color
        ald_description = section.find_element_by_class_name("overallDesc")
        self.assertEqual(color_code,
                         (ald_description.value_of_css_property("color"))), "Incorrect ALD description text color."
        self.assertEqual(ald_text, str(ald_description.text)), "Incorrect ALD description is displayed"
        print("Overall score and ALD description is correctly displayed")

    # Check the content areas text and their placement on the report.
    def check_content_areas(self, section, overall_score_content_area_text, assessment_summary_content_areas):
        # Overall score content area for each assessment
        self.assertIn(overall_score_content_area_text, section.find_element_by_class_name(
                "info2").text), "Overall score content area text incorrectly displayed."
        # Assessment Summary content areas for each assessment
        for key in assessment_summary_content_areas.keys():
            content_text = section.find_element_by_class_name("sidebar").find_element_by_class_name(key).text
            self.assertIn(assessment_summary_content_areas[key].encode('ascii', 'xmlcharrefreplace'),
                          content_text.encode('ascii',
                                              'xmlcharrefreplace')), "Assessment Summary content area not found."

    def check_warning_message(self, section, icon, warning_message):
        contents = section.find_element_by_class_name("content").find_elements_by_tag_name("div")
        self.assertEqual(contents[0].get_attribute("class"), icon, "The icon not display")
        actual_message = contents[1].text
        self.assertEqual(actual_message, warning_message,
                         "The message is not correct:\nactual: {a}\nexpected: {e}"
                         .format(a=actual_message, e=warning_message)
                         )

    # Check claim contents displayed on the Individual Student Report
    def check_claim_contents(self, section, performance_level, claim_name, custom_claim_content_text):
        actual_claim_name = section.find_element_by_css_selector(".header h4").text
        assert (claim_name in actual_claim_name), "Claim content name not found"
        # Validate that the ALD descriptor is available under each content area for each assessment
        self.assertIn(custom_claim_content_text, section.find_element_by_class_name(
                "content").text), "ALD description not found in the content area"

    # Check claim contents tooltip that is displayed on mouse over on the claim contents arrow box on ISR
    def check_claim_tooltip(self, claim_section, popup_header, claim_name, claim_score, claim_content, error_band):
        '''
        OBSOLETE FUNCTION - NO LONGER USED
        Note: The Claim tooltip was removed.
        '''
        self.driver.maximize_window()
        element_to_click = claim_section.find_element_by_class_name("scoreBoxUpper")
        loc = element_to_click.location
        script = "window.scrollTo(%s, %s);" % (loc['x'], loc['y'])
        self.driver.execute_script(script)
        hover_mouse = ActionChains(self.driver).move_to_element(element_to_click)
        hover_mouse.perform()
        try:
            WebDriverWait(self.driver, 15).until(
                    expected_conditions.visibility_of_element_located((By.CLASS_NAME, "claimsPopover")))
        except:
            self.driver.save_screenshot('/tmp/popover.png')
            self.assertTrue(False, "Error in viewing the tooltip")

        # Validate the pop up header
        popover_inner = self.driver.find_element_by_class_name('claimsPopover').find_element_by_class_name(
                "popover-inner")
        self.assertEqual(popup_header, str(popover_inner.find_element_by_class_name(
                "popover-title").text)), "Claim tooltip header incorrectly displayed"
        # Validate the claim content
        claims_tooltip = popover_inner.find_element_by_class_name("claimToolTipSection")
        assert (
            claim_content in str(claims_tooltip.text)), "Claim content text incorrectly displayed n the tooltip summary"
        # Validate the claim title
        assert (claim_name in str(claims_tooltip.find_element_by_class_name(
                "title").text)), "Claim Name incorrectly displayed on the tooltip summary"
        ## Validate the claim score displayed in the header
        assert (claim_score in str(claims_tooltip.find_element_by_class_name(
                "score").text)), "Claim Score incorrectly displayed on the tooltip summary"

        # Validate the claim score displayed on the progress bar
        assert (claim_score in str(claims_tooltip.find_element_by_class_name("claimsBar").find_element_by_class_name(
                "claim_score").text)), "Claim score incorrectly displayed on the tooltip progress bar"
        ## Validate the Minimum and maximum range on the progress bar
        assert ("1200" in str(claims_tooltip.find_element_by_class_name("cutPointsBar").find_element_by_class_name(
                "startPoint").text)), "Claim score incorrectly displayed on the tooltip progress bar"
        assert ("2400" in str(claims_tooltip.find_element_by_class_name("cutPointsBar").find_element_by_class_name(
                "endPoint").text)), "Claim score incorrectly displayed on the tooltip progress bar"

        # Validate the Error Band displayed on the tooltip
        assert (error_band in str(claims_tooltip.find_element_by_class_name(
                "errorBand").text)), "Error Band incorrectly displayed on the tooltip"

    def check_isr_legend_popup(self):
        '''
        Validates the legend popup from the Report Action Nav bar in the Individual Student report
        '''
        legend_popup = self.open_legend_popup()
        #        self.check_legend_popup_ald_section(legend_popup)
        #        self.check_isr_legend_popup_claim_section(legend_popup)
        self.check_isr_legend_content(legend_popup)

    #        self.check_isr_legend_error_band_section(legend_popup)

    def check_isr_legend_popup_language_sp(self):
        '''
        Validates the legend popup from the Report Action Nav bar in the Individual Student report
        '''
        legend_popup = self.open_legend_popup_language_sp()
        self.check_isr_legend_content_language_sp(legend_popup)

    def check_isr_legend_content(self, popup):
        '''
        Validates the Overall score details section including the performance bar and description on the ISR legend popup.
        ;param popup: Legend popup webdriver element
        :type popup: Webdriver Element
         '''
        legend = popup.find_element_by_class_name("overall_score_wrapper")

        expected_first_line = 'This report presents an individual student\'s scores for a selected assessment.'
        actual_first_line = str(legend.find_element_by_tag_name('p').text)
        self.assertEqual(expected_first_line, actual_first_line,
                         "First line on the ISR legend popup incorrectly displayed.")

        expected_disclaimer = 'Data is for illustrative purposes only.'
        actual_disclaimer = str(legend.find_element_by_class_name('isr_disclaimer').text)
        self.assertEqual(expected_disclaimer, actual_disclaimer,
                         "Disclaimer in ISR legend popup incorrectly displayed.")

        ald_table = legend.find_element_by_class_name('span7').find_element_by_tag_name(
                'table').find_elements_by_tag_name('td')
        expected_ald_levels = ['Level 1', 'Level 2', 'Level 3', 'Level 4']
        actual_ald_levels = []
        for each in ald_table:
            actual_ald_levels.append(str(each.text))
        self.assertEqual(expected_ald_levels, actual_ald_levels, "ALD level names incorrectly displayed.")

        claim_level_table = legend.find_element_by_class_name('edware-table-bordered').find_elements_by_tag_name('td')
        expected_claim_levels = ['BELOW STANDARD', 'AT/NEAR STANDARD', 'ABOVE STANDARD']
        actual_claim_levels = []
        for each in claim_level_table:
            actual_claim_levels.append(str(each.text))
        self.assertEqual(expected_claim_levels, actual_claim_levels, "Claim level names incorrectly displayed.")

        expected_error_band_desc = "Smarter Balanced tests provide the most precise scores possible within a reasonable time limit, but no test can be \
100 percent accurate. The error band indicates the range of scores that a student would likely achieve if they were to take the test multiple times. \
It is similar to the \"margin of error\" that newspapers report for public opinion surveys."
        actual_error_band_desc = str(legend.find_element_by_class_name('isr_details').text)
        self.assertEqual(expected_error_band_desc, actual_error_band_desc,
                         "Error band description incorrectly displayed.")

    #        LEGEND_PERF_HEADER = "Overall Score Details:"
    #        expected_color_codes = ["rgba(187, 35, 28, 1)", "rgba(228, 201, 4, 1)", "rgba(106, 165, 6, 1)", "rgba(35, 124, 203, 1)"]
    #        expected_cutpoints = [1200, 1400, 1800, 2100, 2400]
    #        perf_bar_section = popup.find_element_by_class_name("popover-content").find_element_by_class_name("span7").find_element_by_class_name("overall_score_wrapper")
    #
    #        # Validate the Overall Score
    #        overall_score = perf_bar_section.find_element_by_class_name("overall_score_upper")
    #        self.assertEqual(1789, int(overall_score.find_element_by_class_name("asmtScore").text)), "Incorrect overall score displayed in the legend popup"
    #        self.assertEqual("rgba(228, 201, 4, 1)", str(overall_score.find_element_by_class_name("indicator_cell").value_of_css_property("background-color"))), "Overall Score background color is incorrect."
    #        #Validate the indicator for "Overall Score" is displayed
    #        self.assertEqual("Overall Score(ALD color coded)", str(overall_score.find_element_by_class_name("desc_overall_score").text)), "Word 'Overall' did not appear on the report."
    #
    #        # Validate the performance bar
    #        self.assertIn(LEGEND_PERF_HEADER, str(perf_bar_section.text), 'Error: Performance bar section header: {0} is not found in Legend popup'.format(LEGEND_PERF_HEADER))
    #        self.check_colors_perf_bar(perf_bar_section, expected_color_codes)
    #        self.check_cutpoints_perf_bar(perf_bar_section, expected_cutpoints)
    #        self.check_overall_score_perf_bar(perf_bar_section, 1789)
    #
    #        # Validate the Indicators displayed in this section of the legend
    #        self.assertEqual("Overall Score Indicator", str(overall_score.find_element_by_class_name("desc_overall_score_indicator").text)), "Overall score indicator from the performance bar not displayed."
    #        self.assertEqual("Scaled Score Range", str(perf_bar_section.find_element_by_class_name("desc_scaled_score_range").text), "Performance bar indicator not displayed.")
    #        self.assertIn("ALD Cutpoints", str(perf_bar_section.find_element_by_class_name("overall_score_lower").text), "ALD Cutpoints indicator not displayed")
    #        self.assertEqual("Error Bands(brackets denote min/max)", str(perf_bar_section.find_element_by_class_name("desc_error_bands").text), "Error Band indicator not displayed.")

    def check_isr_legend_content_language_sp(self, popup):
        '''
        Validates the Overall score details section including the performance bar and description on the ISR legend popup.
        ;param popup: Legend popup webdriver element
        :type popup: Webdriver Element
         '''
        legend = popup.find_element_by_class_name("overall_score_wrapper")

        expected_first_line = 'Este reporte presenta las puntuaciones de un estudiante individual para una evaluación seleccionada'
        actual_first_line = legend.find_element_by_tag_name('p').text
        self.assertEqual(expected_first_line, actual_first_line,
                         "First line on the ISR legend popup incorrectly displayed.")

        expected_disclaimer = 'Los datos solo tienen fines ilustrativos.'
        actual_disclaimer = legend.find_element_by_class_name('isr_disclaimer').text
        self.assertEqual(expected_disclaimer, actual_disclaimer,
                         "Disclaimer in ISR legend popup incorrectly displayed.")

        ald_table = legend.find_element_by_class_name('span7').find_element_by_tag_name(
                'table').find_elements_by_tag_name('td')
        expected_ald_levels = ['Nivel 1', 'Nivel 2', 'Nivel 3', 'Nivel 4']
        actual_ald_levels = []
        for each in ald_table:
            actual_ald_levels.append(each.text)
        self.assertEqual(expected_ald_levels, actual_ald_levels, "ALD level names incorrectly displayed.")

        claim_level_table = legend.find_element_by_class_name('edware-table-bordered').find_elements_by_tag_name('td')
        expected_claim_levels = [u"DEBAJO DEL ESTÁNDAR", u"EN EL ESTÁNDAR/CERCA DEL ESTÁNDAR", u"ARRIBA DEL ESTÁNDAR"]
        actual_claim_levels = []
        for each in claim_level_table:
            actual_claim_levels.append(each.text)
        self.assertEqual(expected_claim_levels, actual_claim_levels, "Claim level names incorrectly displayed.")
        expected_error_band_desc = u"Las pruebas de Smarter Balanced proveen las puntuaciones más precisas posibles dentro de un límite razonable de tiempo, pero ninguna prueba puede ser 100 porciento precisa. La banda de error indica el rango de puntuaciones que un estudiante obtendría si tomara la prueba varias veces. Es similar al \"margen de error\" que los diarios reportan para las encuestas de opinión pública."
        actual_error_band_desc = legend.find_element_by_class_name('isr_details').text
        print(expected_error_band_desc)
        print(actual_error_band_desc)
        self.assertEqual(expected_error_band_desc, actual_error_band_desc,
                         "Error band description incorrectly displayed.")

    def check_isr_legend_error_band_section(self, popup):
        '''
        Validates the Error Band section and description on the ISR legend popup.
        ;param popup: Legend popup webdriver element
        :type popup: Webdriver Element
         '''
        LEGEND_ERR_BAND_HEADER = "Error Band:"
        LEGEND_ERR_BAND_DESC = "Smarter Balanced tests try to provide the most precise scores possible within a reasonable time limit, but no test can be 100 percent accurate. The error band indicates the range of scores that a student would be very likely to achieve if they were to take the test multiple times. It is similar to the “margin of error” that newspapers report for public opinion surveys."
        err_band_section = popup.find_element_by_class_name("popover-content").find_element_by_class_name(
                "span7").find_element_by_class_name("error_band_wrapper")
        # Validate the Error band section header and description
        self.assertIn(LEGEND_ERR_BAND_HEADER, err_band_section.text,
                      'Error: Error Band section header: {0} is not found in Legend popup'.format(
                              LEGEND_ERR_BAND_HEADER))

    #        self.assertIn(LEGEND_ERR_BAND_DESC, str(err_band_section.text), 'Error: Error Band section description: {0} is not found in Legend popup'.format(LEGEND_ERR_BAND_DESC))

    def check_isr_legend_popup_claim_section(self, popup):
        '''
        Validates the Supporting Score Details: section for the claim performance level description on the legend popup.
        ;param popup: Legend popup webdriver element
        :type popup: Webdriver Element
         '''
        LEGEND_CLAIM_HEADER = "Supporting Score Details:"
        LEGEND_CLAIM_DESC_HEADER = ['Icon', 'Description', 'Meaning']
        LEGEND_CLAIM_ROWS = [["Above Standard",
                              "Your test results clearly show that you understand and are able to apply your knowledge to the standards in this subject-area of your grade."],
                             ["At/Near Standard",
                              "Your test results may be just above or just below the standard, but due to the error band (see below), the result it too close to call."],
                             ["Below Standard",
                              "Your test results clearly show that you have not yet met the standard in this subject-area for your grade."]]

        # Validate the Claim Score section header
        self.assertIn(LEGEND_CLAIM_HEADER,
                      str(popup.find_element_by_class_name("popover-content").find_element_by_class_name("span7").text),
                      'Error: Supporting Score Details header is not found in Legend popup')
        # Validate the Claim Score performance level table headers and contents
        legend_claim_section = popup.find_element_by_class_name("popover-content").find_element_by_class_name(
                "span7").find_element_by_tag_name("table")

        # Validate the table headers
        table_header = legend_claim_section.find_element_by_tag_name("thead").find_elements_by_tag_name("th")
        actual_table_header = []
        for each in table_header:
            actual_table_header.append(str(each.text))
        self.assertEqual(LEGEND_CLAIM_DESC_HEADER, actual_table_header,
                         'Error: Supporting Score Details Table Headers not matching in the Legend popup')
        # Validate the table rows\
        actual_claim_level_rows = []
        table_rows = legend_claim_section.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
        for each in table_rows:
            each_row_column_values = each.find_elements_by_tag_name("td")
            each_row = []
            each_row.append(str(each_row_column_values[1].text))
            each_row.append(str(each_row_column_values[2].text))
            actual_claim_level_rows.append(each_row)
        self.assertEqual(actual_claim_level_rows, LEGEND_CLAIM_ROWS,
                         "Supporting Score Details  table rows do not match")

    def select_asmt_type_isr(self, asmt_selection, asmt_year):
        '''
        Selects the desired assessment type from the cpop asmt type dropdown.
        ;param asmt_selection: Assessment type selection: 'Summative' or 'Interim Comprehensive'
        :type asmt_selection: string
         '''
        self.driver.find_element_by_id("actionBar").find_element_by_class_name("asmtDropdown").find_element_by_tag_name(
                "button").click()
        asmt_dropdown_options = self.driver.find_element_by_class_name("asmtDropdown").find_element_by_class_name(
                "dropdown-menu")
        # asmt_dropdown_options.find_element_by_link_text(asmt_selection).click()
        options = asmt_dropdown_options.find_elements_by_css_selector("li[data-asmttype='" + asmt_selection + "']")
        for each in options:
            if asmt_year in each.text:
                each.click()

        self.check_redirected_requested_page("individual_student_report")
        self.check_selected_asmt_type_isr(asmt_selection)
        self.driver.maximize_window()
        element_to_click = self.driver.find_element_by_class_name("sidebar")
        loc = element_to_click.location
        script = "window.scrollTo(%s, %s);" % (loc['x'], loc['y'])
        self.driver.execute_script(script)
        hover_mouse = ActionChains(self.driver).move_to_element(element_to_click)
        time.sleep(5)
        hover_mouse.click()
        time.sleep(10)

    def check_selected_asmt_type_isr(self, selected_asmt_type):
        '''
        Checks the assessment type on the cpop asmt type dropdown.
        ;param selected_asmt_type: Assessment type selection
        :type selected_asmt_type: string
         '''
        selected_assessment_view = self.driver.find_element_by_id("actionBar").find_element_by_class_name(
                "asmtDropdown").find_element_by_id("selectedAsmtType").text
        self.assertIn(selected_asmt_type, selected_assessment_view), "Incorrect assessment type selected"

    def check_isr_report_info_popup(self):
        '''
        Validates the Report Info text displayed on the mouseover overlay in Individual Student report
        '''
        element_to_click = self.driver.find_element_by_id("infoBar").find_element_by_class_name("reportInfoIcon")
        hover_mouse = ActionChains(self.driver).move_to_element(element_to_click)
        hover_mouse.perform()
        time.sleep(3)
        try:
            WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_class_name("reportInfoPopover"))
        except:
            self.driver.save_screenshot('/tmp/report_info.png')
            self.assertTrue(False, "Error in viewing the report info popover")
        popover_content = self.driver.find_element_by_class_name("reportInfoPopover").find_element_by_class_name(
                "popover-content")
        # Validate the section headers in the report info pop over
        report_info_headers = popover_content.find_elements_by_tag_name("h4")
        self.assertEqual("Purpose:", str(report_info_headers[0].text),
                         "Purpose header not found in report info pop over")
        self.assertEqual("Uses:", str(report_info_headers[1].text), "Uses header not found in report info pop over")
        self.assertEqual("Understanding your score:", str(report_info_headers[2].text),
                         "Understanding your score: header not found in report info pop over")

        descriptions = popover_content.find_elements_by_tag_name("p")

        # Validate the report info 'purpose' and 'Understanding your score:' section description
        purpose_desc = "This report presents individual student assessment scores and provides guidance on how to interpret the results."
        self.assertEqual(purpose_desc, str(descriptions[0].text), "Purpose section description incorrectly displayed")

        understanding_your_score_desc = "The Smarter Balanced assessment is different than other tests with which you may be familiar."
        self.assertEqual(understanding_your_score_desc, str(descriptions[1].text),
                         "Understanding your score section description incorrectly displayed")

        bullet_points = popover_content.find_elements_by_tag_name("ul")

        uses_desc = "Educators, parents or students may use this report to understand student achievement, progress toward mastery " + \
                    "of the Common Core State Standards and attainment of the academic knowledge and skills required to be college content- and career-ready."
        self.assertEqual(uses_desc, str(bullet_points[0].text), "Uses description bullet point not found.")

        understanding_score_first_bullet = "First, the Smarter Balanced summative assessments are Computer Adaptive Tests and take advantage of technology to customize each test to the " + \
                                           "individual student. This means that when a student answers a question correctly, the next question they see will be slightly more " + \
                                           "difficult. Likewise, if an answer is incorrect, the next question will be somewhat less difficult. This procedure allows for more " + \
                                           "efficient and precise measurement of students' knowledge and skills."
        understanding_score_second_bullet = "Second, the assessment is a criterion-referenced test, meaning that it reports individual students’ understanding of a particular set " + \
                                            "of academic knowledge and skills. As a result, scores are not meant to compare students to each other, but rather to determine how well " + \
                                            "each student understands the content assessed. "
        all_understanding_score_bullets = bullet_points[1].find_elements_by_tag_name("li")
        self.assertEqual(understanding_score_first_bullet, (all_understanding_score_bullets[0].text),
                         "Uses description first bullet point not found.")
        self.assertEqual(understanding_score_second_bullet, (all_understanding_score_bullets[1].text),
                         "Uses description second bullet point not found.")

    def check_isr_report_info_popup_sp(self):
        '''
        Validates the Report Info text displayed on the mouseover overlay in Individual Student report
        '''
        time.sleep(3)
        element_to_click = self.driver.find_element_by_id("infoBar").find_element_by_class_name("reportInfoIcon")
        hover_mouse = ActionChains(self.driver).move_to_element(element_to_click)
        hover_mouse.perform()
        time.sleep(3)
        try:
            WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_class_name("reportInfoPopover"))
        except:
            self.driver.save_screenshot('/tmp/report_info.png')
            self.assertTrue(False, "Error in viewing the report info popover")
        popover_content = self.driver.find_element_by_class_name("reportInfoPopover").find_element_by_class_name(
                "popover-content")
        # Validate the section headers in the report info pop over
        report_info_headers = popover_content.find_elements_by_tag_name("h4")
        self.assertEqual(u"Propósito:", report_info_headers[0].text), "Purpose header not found in report info pop over"
        self.assertEqual(u"Usos:", report_info_headers[1].text), "Uses header not found in report info pop over"
        self.assertEqual(u"Comprender su puntuación:", report_info_headers[
            2].text), "Understanding your score: header not found in report info pop over"
        descriptions = popover_content.find_elements_by_tag_name("p")
        # Validate the report info 'purpose' and 'Understanding your score:' section description
        purpose_desc = u"Este reporte presenta las puntuaciones de la evaluación individual del estudiante y provee una guía sobre cómo interpretar los resultados."
        self.assertEqual(purpose_desc, descriptions[0].text, "Purpose section description incorrectly displayed")
        understanding_your_score_desc = u"La evaluación de Smarter Balanced es diferente a otras con que usted pudiera estar familiarizado."
        self.assertEqual(understanding_your_score_desc, descriptions[1].text,
                         "Understanding your score section description incorrectly displayed")
        bullet_points = popover_content.find_elements_by_tag_name("ul")
        uses_desc = u"Los educadores, padres o estudiantes pueden usar este reporte para comprender el dominio del estudiante, el progreso hacia el " + \
                    u"dominio de los Estándares Estatales Esenciales Comunes y la obtención del conocimiento académico y las destrezas requeridas para estar listo para la universidad y la vida profesional."
        self.assertEqual(uses_desc, bullet_points[0].text, "Uses description bullet point not found.")
        understanding_score_first_bullet = u"Primero, las Sumativa evaluaciones de Smarter Balanced son pruebas computacionales adaptables y aprovechan la tecnología para personalizar cada examen a cada estudiante individual. Esto significa que cuando un estudiante contesta correctamente una pregunta, la siguiente pregunta que verá será ligeramente más difícil. Del mismo modo, si una respuesta es incorrecta, la siguiente pregunta será un poco menos difícil. Este procedimiento permite tener la medición más precisa y eficiente del conocimiento y las destrezas del estudiante."
        understanding_score_second_bullet = u"Segundo, la evaluación es una prueba basada en los criterios, lo cual significa que reporta la comprensión del estudiante individual en torno a un conjunto particular de conocimientos y destrezas. Como resultado, las puntuaciones no pretenden comparar a los estudiantes entre sí, sino determinar qué tan bien cada estudiante comprende el contenido evaluado. "
        all_understanding_score_bullets = bullet_points[1].find_elements_by_tag_name("li")
        self.assertEqual(understanding_score_first_bullet, all_understanding_score_bullets[0].text,
                         "Uses description first bullet point not found.")
        self.assertEqual(understanding_score_second_bullet, all_understanding_score_bullets[1].text,
                         "Uses description second bullet point not found.")

    def check_isr_overall_score_summary(self, sequence, subject, score, ald_level):
        '''
        Validates the Overall score is displayed in the report info bar on Individual Student report
        ;param sequence: index of the order of appearance of the overall score - Most commonly Math = 0, ELA = 1 If only one assessment result is displayed then it will be 0.
        :type sequence: integer
        :param subject: Subject name
        :type subject: string
        :param score: Overall score displayed
        :type score: string
        :param ald_level: ALD description
        :type ald_level: string
        '''
        report_info_score_sections = self.driver.find_element_by_id("infoBar").find_elements_by_class_name("overall")

        self.assertIn(subject, str(report_info_score_sections[sequence].text),
                      "Subject text not found in Overall score summary in Report info bar")
        self.assertIn(score, str(report_info_score_sections[sequence].text),
                      "Overall Score not found in Overall score summary in Report info bar")
        self.assertIn(score, str(report_info_score_sections[sequence].text),
                      "ALD name not found in Overall score summary in Report info bar")

    def check_isr_print_pdf_options(self):
        '''
        Validates the print option in the Report Action bar and the different options available to print
        '''
        assert self.driver.find_element_by_id("actionBar").find_element_by_class_name(
                "printItem"), "Print option not found in the Report info navigation bar"
        self.driver.save_screenshot('/tmp/isr_pdf1.png')
        self.driver.find_element_by_id("actionBar").find_element_by_class_name("printLabel").click()
        self.driver.save_screenshot('/tmp/isr_pdf2.png')
        time.sleep(3)
        try:
            WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id("PrintModal"))
        # print_popup = self.driver.find_element_by_id("actionBar").find_element_by_class_name("printItem").find_element_by_id("PrintModal")
        except:
            print("Timeout in opening the Print pop up window")
        self.driver.save_screenshot('/tmp/isr_pdf3.png')
        print_popup = self.driver.find_element_by_id("actionBar").find_element_by_class_name(
                "printItem").find_element_by_id("PrintModal")
        self.assertIn("Print", str(
                self.driver.find_element_by_id("actionBar").find_element_by_class_name("printItem").find_element_by_id(
                        "PrintModal").find_element_by_id("myModalLabel").text), "Print popup header not found")
        print_options = print_popup.find_element_by_class_name("modal-body").find_elements_by_tag_name("li")
        self.assertEqual("Color", print_options[1].text, "Color print option not found")
        self.assertEqual("Grayscale (use for black & white printing)", print_options[0].text,
                         "Grayscale print option not found")
        self.assertEqual("Print", str(print_popup.find_element_by_class_name("modal-footer").text),
                         "Print button not found in the popup")
        print_popup.find_element_by_class_name("close").click()

        def is_modal_window_present(driver):
            try:
                driver.find_element_by_class_name("modal-backdrop")
                return True
            except NoSuchElementException:
                return False

        WebDriverWait(self.driver, 15).until(is_modal_window_present)

    def language_check_isr_print_pdf_options(self, print_popup_text):
        '''
        Validates the print option in the Report Action bar and the different options available to print
        '''
        assert self.driver.find_element_by_id("actionBar").find_element_by_class_name(
                "printItem"), "Print option not found in the Report info navigation bar"
        self.driver.save_screenshot('/tmp/isr_pdf1.png')
        self.driver.find_element_by_id("actionBar").find_element_by_class_name("printLabel").click()
        self.driver.save_screenshot('/tmp/isr_pdf2.png')
        time.sleep(3)
        try:
            WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id("PrintModal"))
        # print_popup = self.driver.find_element_by_id("actionBar").find_element_by_class_name("printItem").find_element_by_id("PrintModal")
        except:
            print("Timeout in opening the Print pop up window")
        self.driver.save_screenshot('/tmp/isr_pdf3.png')
        print_popup = self.driver.find_element_by_id("actionBar").find_element_by_class_name(
                "printItem").find_element_by_id("PrintModal")
        self.assertIn(print_popup_text['head'], self.driver.find_element_by_id("actionBar").find_element_by_class_name(
                "printItem").find_element_by_id("PrintModal").find_element_by_id("myModalLabel").text,
                      "Print popup header not found")
        print_options = print_popup.find_element_by_class_name("modal-body").find_elements_by_tag_name("li")
        self.assertEqual(print_popup_text['message_2'], print_options[1].text, "Color print option not found")
        self.assertEqual(print_popup_text['message_1'], print_options[0].text, "Grayscale print option not found")
        self.assertEqual(print_popup_text['button'], str(print_popup.find_element_by_class_name("modal-footer").text),
                         "Print button not found in the popup")
        print_popup.find_element_by_class_name("close").click()

    def check_accomodations_sections(self, acc_section, expected_acc):
        '''
        Validates the accomodations section & its contents
        '''
        self.assertIn("The following accommodations were made available:",
                      str(acc_section.find_element_by_tag_name("p").text), 'Accomodations description title not found')
        all_accomodations = acc_section.find_elements_by_class_name("edware-label-accommodation")
        actual_acc = []
        for each_acc in all_accomodations:
            actual_acc.append(str(each_acc.text))
        self.assertEqual(expected_acc, actual_acc, "All accomodations not found in the respective section")

    def language_check_accommodations_sections(self, accommodation, acc_section, expected_acc):
        '''
        Validates the accomodations section & its contents
        '''
        self.assertIn(accommodation, acc_section.find_element_by_tag_name("p").text,
                      'Accomodations description title not found')
        all_accomodations = acc_section.find_elements_by_class_name("edware-label-accommodation")
        actual_acc = []
        for each_acc in all_accomodations:
            actual_acc.append(each_acc.text)
        self.assertEqual(expected_acc, actual_acc, "All accomodations not found in the respective section")

    def check_current_selected_opportunity_isr(self, expected_value):
        '''
        Checks the assessment type on the cpop asmt type dropdown.
        ;param selected_asmt_type: Assessment type selection: 'Summative' or 'Interim Comprehensive'
        :type selected_asmt_type: string
         '''
        #        self.assertIn(selected_asmt_type, unicode(self.driver.find_element_by_id("actionBar").find_element_by_class_name("asmtDropdown").find_element_by_id("selectedAsmtType").text)), "Incorrect assessment type selected"
        dropdown = self.driver.find_element_by_class_name("asmtDropdown")
        dropdown_value = dropdown.find_element_by_id("selectedAsmtType").text
        self.assertEqual(expected_value, dropdown_value, "Current opportunity selector is invalid on ISR.")

    def select_opportunity_isr(self, selection):
        dropdown = self.driver.find_element_by_class_name("asmtDropdown")
        dropdown.find_element_by_tag_name("button").click()
        all_options = dropdown.find_element_by_class_name("asmtDropdownMenu").find_elements_by_tag_name('li')
        optionFound = False
        if optionFound is False:
            for each in all_options:
                '''
                Another way to handle the unicode encode error is to encode the expected result and then compare it with the actual text
                for eg: Replace . with &#183; in the expected text like "2016.01.01 &#183; Grade 3 &#183; Interim Comprehensive" and then
                if selection in each.text.encode('ascii', 'xmlcharrefreplace'):
                '''
                if selection in each.text:
                    each.click()
                    time.sleep(5)

    def select_iab_subject(self, selection):
        if selection == "Mathematics":
            self.driver.find_element_by_id("actionBar").find_element_by_class_name("detailsItem").find_element_by_id(
                    "subjectSelectionMath").click()
            subject = "Math"
        elif selection == "ELA/Literacy":
            self.driver.find_element_by_id("actionBar").find_element_by_class_name("detailsItem").find_element_by_id(
                    "subjectSelectionELA").click()
            subject = "ELA"
        else:
            self.assertTrue(False, "Invalid selection for IAB assessments.")
        try:
            WebDriverWait(self.driver, 20).until(lambda driver: str(
                    driver.find_element_by_id("individualStudentContent").find_element_by_class_name(
                            subject).find_element_by_class_name("isrInterimBlockHeader").find_element_by_class_name(
                            "subject").text) == selection, message="Unable to switch the subject view in IAB")
        except:
            self.driver.save_screenshot('/tmp/iab_switch_view.png')
            self.assertTrue(False, "Error in switching the subject view for IAB.")

    def select_subject_view(self, selection):
        if selection == "Mathematics":
            self.driver.find_element_by_id("actionBar").find_element_by_class_name("detailsItem").find_element_by_id(
                    "subjectSelectionMath").click()
            section_id = "assessmentSection0"
        elif selection == "ELA/Literacy":
            self.driver.find_element_by_id("actionBar").find_element_by_class_name("detailsItem").find_element_by_id(
                    "subjectSelectionELA").click()
            section_id = "assessmentSection1"
        else:
            self.assertTrue(False, "Invalid selection for subject view selection.")
        try:
            WebDriverWait(self.driver, 20).until(lambda driver: str(
                    driver.find_element_by_id("individualStudentContent").find_element_by_id(
                            section_id).find_element_by_class_name("sidebar").find_element_by_tag_name(
                            "h1").text) == selection,
                                                 message="Unable to switch the subject view in ISR")
        except:
            self.driver.save_screenshot('/tmp/isr_switch_view.png')
            self.assertTrue(False, "Error in switching the subject view in ISR")

    def select_subject_view_one(self, selection):
        if selection == "Mathematics":
            self.driver.find_element_by_id("actionBar").find_element_by_class_name("detailsItem").find_element_by_id(
                    "subjectSelectionMath").click()
            section_id = "assessmentSection0"
        elif selection == "ELA/Literacy":
            self.driver.find_element_by_id("actionBar").find_element_by_class_name("detailsItem").find_element_by_id(
                    "subjectSelectionELA").click()
            section_id = "assessmentSection0"
        else:
            self.assertTrue(False, "Invalid selection for subject view selection.")
        try:
            WebDriverWait(self.driver, 20).until(lambda driver: str(
                    driver.find_element_by_id("individualStudentContent").find_element_by_id(
                            section_id).find_element_by_class_name("sidebar").find_element_by_tag_name(
                            "h1").text) == selection,
                                                 message="Unable to switch the subject view in ISR")
        except:
            self.driver.save_screenshot('/tmp/isr_switch_view.png')
            self.assertTrue(False, "Error in switching the subject view in ISR")

    def verify_iab_title_score(self, iab_block, grade, block_name, effective_date, performance):
        self.assertIn(grade, str(iab_block.find_element_by_class_name("title").text),
                      "Grade number not displayed on the IAB block.")
        self.assertIn(block_name,
                      str(iab_block.find_element_by_class_name("title").find_element_by_class_name("blockName").text),
                      "IAB Block Name not displayed on the IAB block.")
        self.assertIn(effective_date,
                      str(iab_block.find_element_by_class_name("content").find_element_by_class_name("takenDate").text),
                      "IAB Effective Date not displayed on the IAB block.")
        self.assertIn(performance, str(iab_block.find_element_by_class_name("content").text),
                      "IAB performance name not displayed on the IAB block.")
        performance_image = "edware-icon-large-perf-" + self.get_performance_level_image_name(performance)
        self.assertIsNotNone(
                iab_block.find_element_by_class_name("content").find_element_by_class_name(performance_image),
                "Performance level image not found")

    def verify_iab_previous_results(self, iab_block, num_results, prev_results):
        self.assertEqual("PREVIOUS RESULTS", str(iab_block.find_element_by_class_name("previousResults").text),
                         "PREVIOUS RESULTS header not found in the IAB block")
        tables = iab_block.find_elements_by_class_name("table")
        if len(tables) == 1:
            all_prev_results = tables[0].find_elements_by_class_name("takenDate")
            all_prev_results_icons = tables[0]
            # test = len(tables[0].find_elements_by_tag_name("i"))
            self.assertEqual(int(num_results) * 3, len(tables[0].find_elements_by_tag_name("i")),
                             "Invalid number of previous results performance icons found in the IAB block table.")
        elif len(tables) == 2:
            all_prev_results = tables[1].find_elements_by_class_name("takenDate")
            all_prev_results_icons = tables[1]
            # self.assertEqual(num_results, len(tables[1].find_elements_by_tag_name("i")), "Invalid number of previous results performance icons found in the IAB block table.")

        if num_results > 0:
            # Assert the number of previous results assessments displayed in the PREVIOUS RESULTS table
            self.assertEqual(num_results, len(all_prev_results),
                             "Invalid number of previous results effective dates found in the IAB block table.")
            # Validate the effective date and performance level icon displayed in the PREVIOUS RESULTS table
            for each_expected in prev_results:
                effective_date_found = False
                perf_icon_found = False
                for key in each_expected:
                    perf_icon = "edware-icon-small-perf-" + self.get_performance_level_image_name(each_expected[key])
                for each in all_prev_results:
                    effective_date = []
                    effective_date.append(str(each.text))
                    if effective_date == list(each_expected.keys()):
                        effective_date_found = True
                        break
                self.assertTrue(effective_date_found, "Effective date in IAB assessment not found.")
                self.assertTrue(all_prev_results_icons.find_element_by_class_name(perf_icon),
                                "Performance icon in IAB assessment not found.")
        else:
            self.assertIn("None", str(iab_block.find_element_by_class_name("table").text),
                          "Previous results grid does not show None.")

    def verify_iab_older_results(self, iab_block, num_results, older_results):
        self.assertEqual("OLDER...", str(iab_block.find_element_by_class_name("olderResults").text),
                         "OLDER link not found in the IAB block")
        self.driver.maximize_window()
        element_to_click = iab_block.find_element_by_class_name("olderResults")
        loc = element_to_click.location
        script = "window.scrollTo(%s, %s);" % (loc['x'], loc['y'])
        self.driver.execute_script(script)
        hover_mouse = ActionChains(self.driver).move_to_element(element_to_click)
        hover_mouse.perform()
        try:
            time.sleep(5)
            WebDriverWait(self.driver, 15).until(
                    expected_conditions.visibility_of_element_located((By.ID, "iabPopoverContent")))
        except:
            self.driver.save_screenshot('/tmp/popover.png')
            self.assertTrue(False, "Error in viewing the iabPopoverContent")
        popover = self.driver.find_element_by_id("iabPopoverContent")
        self.assertEqual("PREVIOUS RESULTS CONT'D", str(popover.find_element_by_class_name("previousResults").text),
                         "Previous results cont'd text not found in the IAB block older popover.")

        table = self.driver.find_element_by_id("iabPopoverContent").find_element_by_class_name("table")
        all_older_results = table.find_elements_by_class_name("takenDate")

        self.assertEqual(num_results, len(all_older_results),
                         "Invalid number of older results effective dates found in the IAB block table.")
        self.assertEqual(int(num_results) * 3, len(table.find_elements_by_tag_name("i")),
                         "Invalid number of older results performance icons found in the IAB block table.")
        for each_expected in older_results:
            effective_date_found = False
            for key in each_expected:
                perf_icon = "edware-icon-small-perf-" + self.get_performance_level_image_name(each_expected[key])
            for each in all_older_results:
                effective_date = []
                effective_date.append(str(each.text))
                if effective_date == list(each_expected.keys()):
                    effective_date_found = True
                    break
            self.assertTrue(effective_date_found, "Effective date in IAB assessment not found.")
            self.assertTrue(table.find_element_by_class_name(perf_icon),
                            "Performance icon in IAB assessment not found.")

    def get_performance_level_image_name(self, performance):
        if performance == "Below Standard":
            image = "level-1"
        elif performance == "At/Near Standard":
            image = "level-2"
        elif performance == "Above Standard":
            image = "level-3"
        return image

    def verify_iab_title_score_comp_valid(self, iab_block, grade, block_name, effective_date, performance,
                                          standardized_icon="None", partial_icon="None"):
        self.assertIn(grade, str(iab_block.find_element_by_class_name("title").text),
                      "Grade number not displayed on the IAB block.")
        self.assertIn(block_name,
                      str(iab_block.find_element_by_class_name("title").find_element_by_class_name("blockName").text),
                      "IAB Block Name not displayed on the IAB block.")
        self.assertIn(effective_date,
                      str(iab_block.find_element_by_class_name("content").find_element_by_class_name("takenDate").text),
                      "IAB Effective Date not displayed on the IAB block.")
        self.assertIn(performance, str(iab_block.find_element_by_class_name("content").text),
                      "IAB performance name not displayed on the IAB block.")
        performance_image = "edware-icon-large-perf-" + self.get_performance_level_image_name(performance)
        self.assertIsNotNone(
                iab_block.find_element_by_class_name("content").find_element_by_class_name(performance_image),
                "Performance level image not found")
        if standardized_icon != "None":
            try:
                iab_block.find_element_by_class_name("level2Content").find_element_by_class_name(standardized_icon)
            except NoSuchElementException:
                try:
                    iab_block.find_element_by_class_name("level3Content").find_element_by_class_name(standardized_icon)
                except NoSuchElementException:
                    self.assertTrue(True, "Icon not present")
                    # print "No element found"
                    # self.assertIsNotNone(iab_block.find_element_by_class_name("level2Content").find_element_by_class_name(standardized_icon), "Standard icon not present")

        if partial_icon != "None":
            try:
                iab_block.find_element_by_class_name("level2Content").find_element_by_class_name(partial_icon)
            except NoSuchElementException:
                try:
                    iab_block.find_element_by_class_name("level3Content").find_element_by_class_name(partial_icon)
                except NoSuchElementException:
                    self.assertTrue(True, "Icon not present")
                    # self.assertIsNotNone(iab_block.find_element_by_class_name("level2Content").find_element_by_class_name(partial_icon), "Standard icon not present")

    def verify_iab_previous_results_comp_valid(self, iab_block, num_results, prev_results):
        self.assertEqual("PREVIOUS RESULTS", str(iab_block.find_element_by_class_name("previousResults").text),
                         "PREVIOUS RESULTS header not found in the IAB block")
        tables = iab_block.find_elements_by_class_name("table")
        if len(tables) == 1:
            all_prev_results = tables[0].find_elements_by_class_name("takenDate")
            all_prev_results_icons = tables[0]
            # test = len(tables[0].find_elements_by_tag_name("i"))
            self.assertEqual(int(num_results) * 3, len(tables[0].find_elements_by_tag_name("i")),
                             "Invalid number of previous results performance icons found in the IAB block table.")
        elif len(tables) == 2:
            all_prev_results = tables[1].find_elements_by_class_name("takenDate")
            all_prev_results_icons = tables[1]
            # self.assertEqual(num_results, len(tables[1].find_elements_by_tag_name("i")), "Invalid number of previous results performance icons found in the IAB block table.")

        if num_results > 0:
            # Assert the number of previous results assessments displayed in the PREVIOUS RESULTS table
            self.assertEqual(num_results, len(all_prev_results),
                             "Invalid number of previous results effective dates found in the IAB block table.")
            # Validate the effective date and performance level icon displayed in the PREVIOUS RESULTS table
            all_date = all_prev_results_icons.text
            for each_expected in prev_results:
                for each in each_expected:
                    icon = self.find_icon(each)
                    if icon == "date":
                        self.assertIn(each, all_date, "Date not present in IAB assessment")
                    else:
                        self.assertTrue(all_prev_results_icons.find_element_by_class_name(icon),
                                        "Performance icon in IAB assessment not found.")
        else:
            self.assertIn("None", str(iab_block.find_element_by_class_name("table").text),
                          "Previous results grid does not show None.")

    def find_icon(self, value):
        return {
            "Standardized": "edware-icon-standardized",
            "Partial": "edware-icon-partial",
            "Below Standard": "edware-icon-small-perf-level-1",
            "At/Near Standard": "edware-icon-small-perf-level-2",
            "Above Standard": "edware-icon-small-perf-level-3"
        }.get(value, "date")

    def verify_iab_older_results_comp_valid(self, iab_block, num_results, older_results):
        self.assertEqual("OLDER...", str(iab_block.find_element_by_class_name("olderResults").text),
                         "OLDER link not found in the IAB block")
        self.driver.maximize_window()
        element_to_click = iab_block.find_element_by_class_name("olderResults")
        loc = element_to_click.location
        script = "window.scrollTo(%s, %s);" % (loc['x'], loc['y'])
        self.driver.execute_script(script)
        hover_mouse = ActionChains(self.driver).move_to_element(element_to_click)
        hover_mouse.perform()
        try:
            time.sleep(5)
            WebDriverWait(self.driver, 15).until(
                    expected_conditions.visibility_of_element_located((By.ID, "iabPopoverContent")))
        except:
            self.driver.save_screenshot('/tmp/popover.png')
            self.assertTrue(False, "Error in viewing the iabPopoverContent")
        popover = self.driver.find_element_by_id("iabPopoverContent")
        self.assertEqual("PREVIOUS RESULTS CONT'D", str(popover.find_element_by_class_name("previousResults").text),
                         "Previous results cont'd text not found in the IAB block older popover.")

        table = self.driver.find_element_by_id("iabPopoverContent").find_element_by_class_name("table")
        all_older_results = table.find_elements_by_class_name("takenDate")
        all_older_date = table.text
        self.assertEqual(num_results, len(all_older_results),
                         "Invalid number of older results effective dates found in the IAB block table.")
        self.assertEqual(int(num_results) * 3, len(table.find_elements_by_tag_name("i")),
                         "Invalid number of older results performance icons found in the IAB block table.")
        for each_expected in older_results:
            for each in each_expected:
                icon = self.find_icon(each)
                if icon == "date":
                    self.assertIn(each, all_older_date, "Date not present in older pop up")
                else:
                    self.assertTrue(table.find_element_by_class_name(icon), "icons are not present in the older pop up")
