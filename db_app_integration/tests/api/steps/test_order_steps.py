from fastapi.testclient import TestClient
from pytest_bdd import scenarios, parsers, given, when, then

scenarios("../features/orders.feature")


@given(parsers.parse('a user exists with ID {user_id:d}'))
def given_user_exist(context:dict, user_id:int):
    context["payload"] = {"user_id":user_id}

@given(parsers.parse('I have an order payload with item_name "{item_name}" and price {price:d}'))
def given_create_payload(context:dict, item_name:str, price:int):
    context["payload"].update({"item_name":item_name,"price":price})

@when(parsers.parse('I send POST request to "{path}"'))
def when_req_sent(client:TestClient, context:dict, path:str):
    payload = context["payload"]
    response = client.post(path,json=payload)
    context["response"] = response

@then(parsers.parse('the response status code should be {code:d}'))
def then_verify_res_status_code(context:dict, code:int):
    response = context["response"]
    assert response.status_code == code

@then(parsers.parse('the response should contain item_name "{item_name}" and price {price:d}'))
def then_verify_res_data(context:dict, item_name:str, price:int):
    response = context["response"].json()
    assert response["item_name"] == item_name
    assert response["price"] == price

#Scenario 2

@given(parsers.parse('no user exists with ID {user_id:d}'))
def given_invalid_user_exist(context:dict, user_id:int):
    context["payload"] = {"user_id":user_id}

@then(parsers.parse('the response message should be "{message}"'))
def then_validate_res_message(context:dict, message:str):
    response = context["response"].json()
    assert response["detail"] == message

#Scenario 3

@given(parsers.parse('an order exists with user ID {user_id:d}'))
def given_order_exist(context:dict, user_id:int):
    pass

@when(parsers.parse('I send GET request to "{path}"'))
def when_get_req_sent(client:TestClient, context:dict, path:str):
    response = client.get(path)
    context["response"] = response

@then(parsers.parse('the response should contain user ID {user_id:d}'))
def then_order_contain_user_id(context:dict, user_id:int):
    response = context["response"].json()
    for order in response:
        assert order["user_id"] == user_id