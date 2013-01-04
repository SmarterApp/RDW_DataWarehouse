import unittest
from pyramid import testing
from sbacpoc.views import my_view, my_templateview


class TestViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info['project'], 'sbacpoc')

    def test_my_templateview(self):
        request = testing.DummyRequest()
        response = my_templateview(request)
        expected_json = {
                            "data": {
                                "account": {
                                    "code": "1209",
                                    "name": "MCPS Account"
                                },
                                "scope_groups": {
                                    "teacher": "Def",
                                    "grade_groups": "Grade",
                                    "school_group_type": "Type",
                                    "school_group": "Group",
                                    "section": "Xyz",
                                    "school": "Abc"
                                }
                            },
                            "report_id": 1,
                            "parameters": {
                                "selected": "selected",
                                "all": "all",
                                "selected_rows": "rows"
                            }
                        }
        self.assertEqual(response, expected_json)


if __name__ == '__main__':
    unittest.main()
