from fastapi.testclient import TestClient
from pytest_bdd import scenarios, parsers, given, when, then

scenarios("../features/profile.feature")

@given(parsers.parse('a user exists with ID {user_id:d}'))
def given_user_id_exists(client:TestClient, user_id:int):
    user = client.get(f"/users/id/{user_id}")
    assert user.status_code == 200

@given(parsers.parse('I have a profile payload with user_id {user_id:d} and bio "{bio_data}"'))
def given_profile_payload(context:dict, user_id:int, bio_data:str):
    context["payload"] = {"user_id":user_id, "bio":bio_data}

@when(parsers.parse('I send POST request to "{path}"'))
def when_req_sent(client:TestClient, context:dict, path:str):
    payload = context["payload"]
    response = client.post(path, json=payload)
    context["response"] = response

@then(parsers.parse('the response status code should be {code:d}'))
def then_verify_res_status(context:dict, code:int):
    res_status_code = context["response"].status_code
    assert res_status_code == code

@then(parsers.parse('the response should contain user_id {user_id:d} and bio "{bio_data}"'))
def then_verify_res_details(context:dict, user_id:int, bio_data:str):
    res_data = context["response"].json()
    assert res_data["user_id"] == user_id
    assert res_data["bio"] == bio_data

#Scenario 2
@given(parsers.parse('no user exists with ID {user_id:d}'))
def given_user_not_exist(user_id:int):
    pass

@then(parsers.parse('the response message should be "{message}"'))
def then_verify_profile_res(context:dict, message:str):
    response_msg = context["response"].json()["detail"]
    assert response_msg == message

#Scenario 3
@given(parsers.parse('a profile already exists for user ID {user_id:d}'))
def given_profile_already_exist(user_id:int):
    pass

#Scenario 4
@when(parsers.parse('I send GET request to "{path}"'))
def when_user_id_get_profile(client:TestClient, context:dict, path:str):
    response = client.get(path)
    context["response"] = response

@then(parsers.parse('the response should contain user_id {user_id:d}'))
def then_profile_consist_user_id(context:dict, user_id:int):
    res_user_id = context["response"].json()["user_id"]
    assert res_user_id == user_id