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

import allure

from edware_testing_automation.frontend_tests.indiv_student_helper import IndividualStudentHelper
from edware_testing_automation.frontend_tests.los_helper import LosHelper
from edware_testing_automation.pytest_webdriver_adaptor.pytest_webdriver_adaptor import browser


@allure.feature('Smarter: Multi languages support')
class LanguageIndividualStudentReport(IndividualStudentHelper, LosHelper):
    """
    Tests for Individual Student Report
    """

    def __init__(self, *args, **kwargs):
        IndividualStudentHelper.__init__(self, *args, **kwargs)
        LosHelper.__init__(self, *args, **kwargs)

    def setUp(self):
        """ setUp: Open webpage """
        self.open_requested_page_redirects_login_page("state_view_sds")
        # login as a parent
        # self.enter_login_credentials("arice", "arice1234")
        self.enter_login_credentials("gman", "gman1234")
        self.check_redirected_requested_page("state_view_sds")
        # Select Spanish language
        self.select_language("es")

    @allure.story('Student view page')
    def test_grade_3_individual_student_report_Spanish(self):
        cutpoints = [1200, 1400, 1800, 2100, 2400]
        expected_color_codes = ["rgba(187, 35, 28, 1)", "rgba(228, 201, 4, 1)", "rgba(106, 165, 6, 1)",
                                "rgba(35, 124, 203, 1)"]
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("242", "ui-jqgrid-ftable")
        self.drill_down_navigation("03", "jqgfirstrow")
        # Click on 'Lettie L Hose' student link from list of students
        self.drill_down_navigation("jqg26", "overallScoreSection")
        breadcrumb_list = ["North Carolina", "Sunset School District", "Sunset - Eastern Elementary", "Grado 03"]

        self.check_breadcrumb_hierarchy_links(breadcrumb_list)
        self.check_breadcrumb_trail("Lettie L. Hose's Results")

        self.check_headers_language("Guy Man", "Salir")
        self.check_page_header("Lettie L. Hose | Grado 03")
        self.check_isr_overall_score_summary(0, 'Mathematics', '1800', "Nivel 3")
        self.check_isr_overall_score_summary(1, 'ELA/Literacy', '2200', "Nivel 4")
        self.check_current_subject_view("Mathematics")

        math_assmnt_info = browser().find_element_by_class_name("sidebar")
        self.assertIn('Mathematics', math_assmnt_info.text)
        self.assertIn('Summative 2015 - 2016', math_assmnt_info.text)
        self.assertIn('Fecha de administración: 4/10/2016', math_assmnt_info.text)

        math_perf_bar = browser().find_element_by_id("individualStudentContent").find_element_by_class_name(
            "confidenceLevel")
        math_overall_score = 1800
        self.check_overall_score_perf_bar(math_perf_bar, math_overall_score)
        self.check_cutpoints_perf_bar(math_perf_bar, cutpoints)
        self.check_colors_perf_bar(math_perf_bar, expected_color_codes)

        math_overall_score_section = browser().find_element_by_id(
            "individualStudentContent").find_element_by_class_name("overallScoreSection")
        self.check_overall_Score_ald(math_overall_score_section, 1800, "rgba(106, 165, 6, 1)", "Puntuación general",
                                     "Nivel 3")

        math_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection0")
        math_overall_score_content = "El estudiante ha cumplido con el estándar de rendimiento y demuestra " \
                                     "un progreso hacia el dominio del conocimiento y las destrezas en matemáticas " \
                                     "necesarios para el éxito en cursos futuros."
        # math_overall_score_content = unicode(math_overall_score_content.decode("iso-8859-4"))
        # To update the assessmentSummarySection dictionary: From 'assesmentSummary' class: {class name: text}
        math_left_pane_content = {
            "psychometric": "Los niveles de rendimiento representan las calificaciones de los estudiantes en la "
                            "evaluación y las fortalezas y las áreas de oportunidad de los estudiantes. "
                            "Los resultados del examen son una de muchas medidas del rendimiento académico "
                            "de un estudiante."
        }
        self.check_content_areas(math_content_area, math_overall_score_content, math_left_pane_content)

        math_claim_content = browser().find_element_by_id("individualStudentContent").find_element_by_class_name(
            "claimsSection").find_elements_by_class_name("claims")
        self.check_claim_contents(math_claim_content[0], "Below Standard", str("Conceptos y procedimientos"),
                                  "Los estudiantes pueden explicar y aplicar conceptos matemáticos y realizar "
                                  "procedimientos matemáticos con precisión y dominio.")
        self.check_claim_contents(math_claim_content[1], "At/Near Standard ",
                                  str("Resolución de problemas y análisis de datos"),
                                  "Los estudiantes pueden resolver un rango de problemas complejos bien planteados "
                                  "en matemáticas puras y aplicadas, usando productivamente el conocimiento "
                                  "y las estrategias de resolución de problemas. Los estudiantes pueden analizar "
                                  "escenarios complejos de la vida real y pueden construir y usar modelos "
                                  "matemáticos para interpretar y resolver problemas.")
        self.check_claim_contents(math_claim_content[2], "Above Standard ", str("Razonamiento para comunicarse"),
                                  "Los estudiantes pueden construir con claridad y precisión argumentos viables para "
                                  "apoyar su propio razonamiento y para criticar el razonamiento de otros.")

        math_expected_accomodations = ['Braille', 'Elementos impresos', 'Lenguaje de señas norteamericano',
                                       'Modo de optimizar',
                                       'Pasajes/estímulos impresos', 'Reguladores de ruido',
                                       'Tabla de multiplicación', 'Ábaco']
        acc_title = browser().find_element_by_id("individualStudentContent").find_element_by_class_name(
            "accommodationSection").find_element_by_class_name("content").find_element_by_tag_name("h4")
        self.assertIn(str("Adaptaciones"), str(acc_title.text), 'Accomodations header in the section not found.')
        math_all_acc_section = browser().find_element_by_id("individualStudentContent").find_element_by_class_name(
            "accommodationSection").find_element_by_class_name("section")
        accom_text = u"Las siguientes adaptaciones se hicieron disponibles:"
        self.language_check_accommodations_sections(accom_text, math_all_acc_section, math_expected_accomodations)

        self.select_subject_view("ELA/Literacy")
        self.check_current_subject_view("ELA/Literacy")

        ela_assmnt_info = browser().find_element_by_id("assessmentSection1").find_element_by_class_name("sidebar")
        self.assertIn('ELA/Literacy', ela_assmnt_info.text)
        self.assertIn('Summative 2015 - 2016', ela_assmnt_info.text)
        self.assertIn('Fecha de administración: 4/10/2016', ela_assmnt_info.text)

        ela_perf_bar = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1").find_element_by_class_name("confidenceLevel")
        ela_overall_score = 2200
        self.check_overall_score_perf_bar(ela_perf_bar, ela_overall_score)
        self.check_cutpoints_perf_bar(ela_perf_bar, cutpoints)
        self.check_colors_perf_bar(ela_perf_bar, expected_color_codes)

        ela_overall_score_section = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1").find_element_by_class_name("overallScoreSection")
        self.check_overall_Score_ald(ela_overall_score_section, 2200, "rgba(35, 124, 203, 1)", "Puntuación general",
                                     "Nivel 4")

        ela_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1")
        ela_overall_score_content = "El estudiante ha excedido el estándar de rendimiento y demuestra un progreso " \
                                    "avanzado hacia el dominio del conocimiento y las destrezas en artes del " \
                                    "lenguaje/alfabetización necesarios para el éxito en cursos futuros."
        ela_left_pane_content = {
            "psychometric": "Los niveles de rendimiento representan las calificaciones de los estudiantes en "
                            "la evaluación y las fortalezas y las áreas de oportunidad de los estudiantes. "
                            "Los resultados del examen son una de muchas medidas del rendimiento académico "
                            "de un estudiante."}
        self.check_content_areas(ela_content_area, ela_overall_score_content, ela_left_pane_content)

        ela_claim_content = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1").find_element_by_class_name("claimsSection").find_elements_by_class_name("claims")
        self.check_claim_contents(ela_claim_content[0], "Above Standard", "Lectura",
                                  "Los estudiantes pueden leer con atención y de manera analítica para comprender "
                                  "un rango de textos literarios e informativos de complejidad ascendente.")
        self.check_claim_contents(ela_claim_content[1], "Below Standard", "Escritura",
                                  "Los estudiantes pueden producir escritos efectivos y bien fundamentados para un "
                                  "rango de propósitos y audiencias.")
        self.check_claim_contents(ela_claim_content[2], "Below Standard", str("Comprensión auditiva"),
                                  "Los estudiantes pueden emplear destrezas efectivas del habla y auditivas para un "
                                  "rango de propósitos y audiencias.")
        self.check_claim_contents(ela_claim_content[3], "Below Standard", str("Investigación y consulta"),
                                  "Los estudiantes pueden participar en estudios y búsquedas para investigar temas y "
                                  "para analizar, integrar y presentar información.")

        ela_expected_accomodations = ['Elementos impresos', 'Lenguaje de señas norteamericano', 'Modo de optimizar',
                                      'Pasajes/estímulos impresos',
                                      'Reguladores de ruido', 'Respuesta alternativa', 'Texto a habla',
                                      'Voz a texto']
        ela_all_acc_section = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1").find_element_by_class_name("accommodationSection").find_element_by_class_name(
            "section")
        accom_ela_text = "Las siguientes adaptaciones se hicieron disponibles:"
        self.language_check_accommodations_sections(accom_ela_text, ela_all_acc_section, ela_expected_accomodations)

        self.check_help_popup_language_sp()
        self.check_isr_legend_popup_language_sp()
        self.check_isr_report_info_popup_sp()

    @allure.story('Student view page')
    def test_grade_8_individual_student_report_Spanish(self):
        # Click on 'Sunset - Western Middle - Grade 8' school link from list of districts
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("245", "ui-jqgrid-ftable")
        self.drill_down_navigation("08", "jqgfirstrow")
        self.select_academic_year_los_language(1,
                                               "Usted está viendo un año académico anterior. Regrese al 2015 - 2016.",
                                               "2014 - 2015")
        self.total_los_records(3)
        # Click on 'Wall E. Bass'' student link from list of students
        self.drill_down_navigation("jqg40", "overallScoreSection")

        self.check_page_header("Wall E. Bass | Grado 08")
        self.check_isr_overall_score_summary(0, 'Mathematics', '1967', "Nivel 3")
        self.check_isr_overall_score_summary(1, 'ELA/Literacy', '1373', "Nivel 1")

        math_section = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection0")
        math_overall_score_content = "El estudiante ha cumplido con el estándar de rendimiento y demuestra un " \
                                     "progreso hacia el dominio del conocimiento y las destrezas en matemáticas " \
                                     "necesarios para el éxito en cursos universitarios acreditados de nivel " \
                                     "básico después de la escuela secundaria."
        math_left_pane_content = {
            "psychometric": "Los niveles de rendimiento representan las calificaciones de los estudiantes en "
                            "la evaluación y las fortalezas y las áreas de oportunidad de los estudiantes. "
                            "Los resultados del examen son una de muchas medidas del rendimiento académico "
                            "de un estudiante."}
        self.check_content_areas(math_section, math_overall_score_content, math_left_pane_content)

        self.select_subject_view("ELA/Literacy")
        self.check_current_subject_view("ELA/Literacy")
        ela_section = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1")
        ela_overall_score_content = "El estudiante no ha alcanzado el estándar de rendimiento y necesita una " \
                                    "mejora sustancial para demostrar el conocimiento y las destrezas en artes " \
                                    "del lenguaje/alfabetización necesarios para el éxito en cursos universitarios " \
                                    "acreditados de nivel básico después de la escuela secundaria."
        ela_left_pane_content = {
            "psychometric": "Los niveles de rendimiento representan las calificaciones de los estudiantes en la "
                            "evaluación y las fortalezas y las áreas de oportunidad de los estudiantes. "
                            "Los resultados del examen son una de muchas medidas del rendimiento académico "
                            "de un estudiante."}
        self.check_content_areas(ela_section, ela_overall_score_content, ela_left_pane_content)

    @allure.story('Student view page')
    def test_grade_11_individual_student_report(self):
        # Click on 'Sunset - Central High - Grade 11' link from list of states
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("248", "ui-jqgrid-ftable")
        self.drill_down_navigation("11", "jqgfirstrow")
        self.drill_down_navigation("jqg21", "overallScoreSection")

        self.check_page_header("Henry Clauson | Grado 11")
        self.check_isr_overall_score_summary(0, 'Mathematics', '2399', "Nivel 4")
        self.check_isr_overall_score_summary(1, 'ELA/Literacy', '1428', "Nivel 2")

        math_section = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection0")
        math_overall_score_content = "El estudiante ha excedido el estándar de rendimiento y demuestra el " \
                                     "conocimiento y las destrezas en matemáticas necesarios para el éxito " \
                                     "en cursos universitarios acreditados de nivel básico después de la " \
                                     "escuela secundaria."
        math_left_pane_content = {
            "psychometric": "Los niveles de rendimiento representan las calificaciones de los estudiantes "
                            "en la evaluación y las fortalezas y las áreas de oportunidad de los estudiantes. "
                            "Los resultados del examen son una de muchas medidas del rendimiento académico de "
                            "un estudiante.",
            "policy": "Los colegios y las universidades pueden usar las puntuaciones de Smarter Balanced como "
                      "evidencia de la preparación del estudiante para los cursos de nivel de entrada que "
                      "tienen crédito. Para mayor información, visite http://www.ncgov.com/"}
        self.check_content_areas(math_section, math_overall_score_content, math_left_pane_content)

        self.select_subject_view("ELA/Literacy")
        self.check_current_subject_view("ELA/Literacy")
        ela_section = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1")
        ela_overall_score_content = "El estudiante casi alcanza el estándar de rendimiento y tal vez requiera " \
                                    "un mayor desarrollo para demostrar el conocimiento y las destrezas en artes " \
                                    "del lenguaje/alfabetización necesarios para el éxito en cursos universitarios " \
                                    "acreditados de nivel básico después de la escuela secundaria."
        ela_left_pane_content = {
            "psychometric": "Los niveles de rendimiento representan las calificaciones de los estudiantes en la "
                            "evaluación y las fortalezas y las áreas de oportunidad de los estudiantes. "
                            "Los resultados del examen son una de muchas medidas del rendimiento académico "
                            "de un estudiante.",
            "policy": "Los colegios y las universidades pueden usar las puntuaciones de Smarter Balanced como "
                      "evidencia de la preparación del estudiante para los cursos de nivel de entrada que "
                      "tienen crédito. Para mayor información, visite http://www.ncgov.com/"}
        self.check_content_areas(ela_section, ela_overall_score_content, ela_left_pane_content)
        print_popup_text = {'head': 'Imprimir',
                            'message_1': 'Escala de grises (usar para imprimir en blanco y negro)',
                            'message_2': 'Color', 'button': 'Imprimir'}
        self.language_check_isr_print_pdf_options(print_popup_text)

        # Check any random CA 11th grader gets the default higher ed link
        print("Grade 11 Individual Student Report: Testing higher ed link for CA")
        current_url = browser().current_url
        domain = current_url.split("/assets/")
        california_url = domain[0] + "/assets/html/comparingPopulations.html?stateCode=CA"
        browser().get(california_url)
        # # Click on district
        # self.drill_down_navigation("229", "ui-jqgrid-ftable")
        # self.drill_down_navigation("942", "ui-jqgrid-ftable")
        # self.drill_down_navigation("11", "jqgfirstrow")
        # self.select_academic_year_los_language(1, "Usted está viendo un año académico anterior. "
        #                                           "Regrese al 2015 - 2016.", "2014 - 2015")
        # self.drill_down_navigation("jqg20", "overallScoreSection")
        # print("Check that default higher-ed link appears for CA")
        # left_pane_content = "Los colegios y las universidades pueden usar las puntuaciones de Smarter " \
        #                     "Balanced como evidencia de la preparación del estudiante para los cursos " \
        #                     "de nivel de entrada que tienen crédito. Para mayor información, " \
        #                     "visite http://www.smarterbalanced.org/higher-education/"
        # content_text = browser().find_element_by_id("individualStudentContent")\
        #     .find_element_by_id("assessmentSection1").find_element_by_class_name("sidebar")\
        #     .find_element_by_class_name("policy").text
        # self.assertIn(left_pane_content, content_text), "Left lane CA content area not found."

    @allure.story('State view page')
    def test_download_popup_content(self):
        export_popup = self.open_file_download_popup("Descargar")
        # Reading the heading and verify
        headings = export_popup.find_elements_by_class_name("marginLeft8")
        expected_headings = ['Vista actual', 'Resultados de la evaluación del estudiante',
                             'Reportes del estudiante imprimibles', 'Descargas del estado']
        actual_headings = []
        for each in headings:
            actual_headings.append(each.text)
        self.assertEqual(expected_headings, actual_headings, "headings are not proper")
        # Reading the contents and verify
        contents = export_popup.find_elements_by_tag_name("p")
        self.assertEqual(contents[0].text, 'Descargar la vista actual en formato CSV.', "content is not proper")
        self.assertEqual(contents[1].text,
                         'Descargar resultados de evaluación para todos los estudiantes en este estado.',
                         "content is not proper")
        self.assertEqual(contents[5].text,
                         'No disponible. Haga clic en una escuela para descargar reportes individuales del estudiante.',
                         "content is not proper")
        self.assertEqual(contents[8].text, 'Descargar reportes de registro y extractos XML.', "content is not proper")
        # Reading the notes and verify
        self.assertEqual(export_popup.find_element_by_class_name("note").find_element_by_tag_name("p").text,
                         'Nota: Las descargas de arriba reflejarán cualquier selección que haya hecho, incluyendo el '
                         'año académico, evaluaciones y filtros.',
                         "text is not proper")
