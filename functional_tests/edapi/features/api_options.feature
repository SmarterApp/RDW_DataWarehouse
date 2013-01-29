Feature: OPTIONS request for Individual Student Report Service
getting the report schema
list of available HTTP methods


Scenario:  OPTIONS request to endpoint: individual_student_report
	Given I send a "OPTIONS" request to "/data/individual_student_report"
	Then the response code is "200"
	Then the response body I should only see the following fields:
	|FieldName						|
	|studentId						|
	|assessmentId					|
	Then in "assessmentId" I should only see the following fields and values:
	|FieldName	|Value 									    |
	|name				|student_assessments_report	|
	|type				|integer										|
	|required		|false											|
	Then in "studentId" I should only see the following fields and values:
	|FieldName			|Value		|
	|type				    |integer	|
	|required			  |true		  |

Scenario:  OPTIONS request to endpoint: student_assessments_report
	Given I send a "OPTIONS" request to "/data/student_assessments_report"
	Then the response code is "200"
	Then in "studentId" I should only see the following fields and values:
	|FieldName	|Value		|
	|type				|integer	|
	|required		|True	  	|	
	
Scenario:  OPTIONS request to an invalid endpoint
	Given I send a "OPTIONS" request to "/data/dummy_report"
	Then the response code is "404"
	Then the response body has an error message "Report dummy_report is not found"
