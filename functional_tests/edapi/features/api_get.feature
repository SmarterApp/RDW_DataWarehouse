Feature: GET Request for Individual Student Report Service

Scenario: GET request
	Given I send a "GET" request to "/data"
	Then the response code is "200"
	Then the response body has "3" elements
	# Then the response body contains the following fields:
	Then the response body I should only see the following fields:
	|FieldName						        |
	|list_of_students             |
	|student_assessments_report		|
	|individual_student_report		|

Scenario: GET request with an invalid endpoint	
	Given I set request header of "content-type" with value "application/json"
	Given I send a "GET" request to "/dummy"
	Then the response code is "404"
	
Scenario: GET request with an invalid content-type	
	Given I set request header of "content-type" with value "text/plain"
	Given I send a "GET" request to "/data/individual_student_report"
	Then the response code is "404"
	
Scenario: GET request with an invalid parameters	
	Given I set request header of "content-type" with value "application/json"
	Given I send a "GET" request to "/data/individual_student_report"
	Then the response code is "412"

Scenario: GET request with valid parameters	
	Given I set request header of "content-type" with value "application/json"	
	Given I send a "GET" request to "/data/individual_student_report?studentId=1001&assessmentId=1"
	Then the response code is "200"
	Then the response body has "1" elements
	Then the response body for all entities I should see the following fields:
	|FieldName			       |
	|asmt_period			     |
	|asmt_claim_2_score		 |
	|asmt_claim_4_name		 |
	|asmt_claim_3_name		 |
	|last_name			       |
	|asmt_claim_1_name	   |
	|asmt_claim_4_score		 |
	|asmt_claim_1_score    |
	|asmt_claim_3_score    |
	|first_name            |
	|asmt_claim_2_name     |
	|asmt_score            |
	|student_id            |
	|asmt_subject          |
	|middle_name           |
	