from behave import *
import requests
import json
from hamcrest import *

SMARTER_URL = "http://0.0.0.0:6543"

class Request(dict):
    def __init__(self):
        pass 

#Instantiate an object of Request class
def set_up_request(context):
    req = getattr(context, "request", None) 
    if (req is None):
        context.request = Request()

@given('I send a "{verb}" request to "{end_point}"')
def options_request(context, verb, end_point):
    set_up_request(context)
    if (verb == "OPTIONS"):
        context.response = requests.options(SMARTER_URL + end_point)
    elif (verb == "GET"):
        context.response = requests.get(SMARTER_URL + end_point, **context.request)       
    elif (verb == "POST"):
        context.response = requests.post(SMARTER_URL + end_point, **context.request)
    else:
        print("Error: Entered an invalid request verb: " + verb)
    
@then('the response code is "{code}"')
def check_response_code(context, code):
    expected = str(context.response.status_code)
    assert_that(expected, is_(code), 'Actual return code: {0} Expected: {1}'.format(expected, code))
  
# Validate the fields in the JSON response
@then('the response body I should only see the following fields')
def check_resp_body_fields(context):
    check_number_of_fields(context, context.response.json())
    print (context.response.json())
    check_contains_fields(context, context.response.json())

# Check for the fields and values only for the given entity
@then('in "{entity}" I should only see the following fields and values')
def check_response_fields_values(context, entity):
    context.entities_to_check = []
    print(context.entities_to_check)
    recursively_get_map(context, context.response.json(), entity)
    print("..")
    for row in context.entities_to_check:
        check_contains_fields(context, row, True)
        check_number_of_fields(context, row)

# Check for the fields for all the entities       
@then('the response body for all entities I should see the following fields')
def check_each_entity_in_body_for_fields(context):
    for row in context.response.json():
        check_contains_fields(context, row)
        check_number_of_fields(context, row)

# Check for the fields only for the given entity        
@then('in "{entity}" I should only see the following fields')
def check_entity_fields(context, entity):
    context.entities_to_check = []    
    recursively_get_map(context, context.response.json(), entity)
    for row in context.entities_to_check:
        check_contains_fields(context, row)
        check_number_of_fields(context, row)
        
@given('I set request header of "{key}" with value "{value}"')
def set_request_header(context, key, value):
    set_up_request(context)
    context.request['headers'] = { key : value }
  
@given('I set payload to "{payload}"')
def set_payload(context, payload):
    set_up_request(context)
    context.request['data'] = payload
    
@then('the response body has "{size}" elements')
def check_resp_body(context, size):
    json_body = context.response.json()
    assert_that((type(json_body) is list), "Response body is not a list")
    assert_that(len(json_body), equal_to(int(size)), 'Actual size: {0} Expected: {1}'.format(len(json_body), size))
        
@then('the response body has an error message "{msg}"')
def check_resp_error(context, msg):
    json_body = context.response.json()
    assert_that(json_body['error'], equal_to(msg))
    
################################################################################
# Helper methods
################################################################################
# Check that each 'map' has the correct fields
def check_contains_fields(context, body, verifyValue = False):
    for row in context.table:
        assert_that(row['FieldName'] in body, "{0} is not found".format(row['FieldName']))
        if (verifyValue):
            print(row['Value'])
            print(str(body[row['FieldName']]))
            assert_that(row['Value'].lower(), equal_to(str(body[row['FieldName']]).lower()), "{0} is not found".format(row['Value']))
        
# Check that each 'map' has the correct number of fields
def check_number_of_fields(context, body):
    expected_count = len(context.table.rows)
    actual_count = len(body)
    assert_that(actual_count, equal_to(expected_count))

# key is a string, dictionary based, separated by :
# Map is the data from the table from the test steps (Feature file)
def recursively_get_map(context, body, key): 
    keys = key.split(':')
    if (type(body) is dict):
        assert_that(keys[0] in body, "{0} is not found".format(keys[0]))
        if (len(keys) > 1):
            recursively_get_map(context, body[keys[0]], keys.pop(0).join(':'))
        else:
            context.entities_to_check.append(body[keys[0]])
    elif (type(body) is list):
        for elem in body:
            assert_that(keys[0] in elem)
            if (len(keys) > 1):
                pass
                recursively_get_map(context, elem[keys[0]], keys.pop(0).join(':'))
            else:
                context.entities_to_check.append(elem[keys[0]])

