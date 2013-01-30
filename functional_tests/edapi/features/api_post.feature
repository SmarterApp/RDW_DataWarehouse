Feature: POST request for Individual Student Report Service

Scenario:  POST request with invalid content-type
	Given I set request header of "content-type" with value "text/html"
	Given I send a "POST" request to "/data/individual_student_report"
	Then the response code is "401"

Scenario:  POST request with Valid content-type but no payload information
	Given I set request header of "content-type" with value "application/json"
	Given I send a "POST" request to "/data/individual_student_report"
	Then the response code is "412"
	Then the response body has an error message "Invalid Parameters"
	
Scenario:  POST request with Valid content-type but Invalid payload information		
	Given I set request header of "content-type" with value "application/json"
	Given I set payload to "{"studentId":"abc"}"
	Given I send a "POST" request to "/data/individual_student_report"
	Then the response code is "412"

Scenario:  POST request with Valid content-type but Valid payload information	
	Given I set request header of "content-type" with value "application/json"
	Given I set payload to "{"studentId": 1001,"assessmentId": 1}"
	Given I send a "POST" request to "/data/individual_student_report"
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
	
