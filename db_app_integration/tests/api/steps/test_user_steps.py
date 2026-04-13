from fastapi.testclient import TestClient
from pytest_bdd import scenarios, parsers, given, when, then

scenarios("../features/users.feature")

@given(parsers.parse('I have a user payload with name "{name}" and email "{email}"'))
def user_payload(context:dict, name:str, email:str):
    # Store payload in context
    context['payload'] = {
        "name": name,
        "email": email
    }

@when(parsers.parse('I send POST request to "{path}"'))
def send_post_request(client:TestClient, context:dict, path:str):
    response = client.post(path, json=context.get('payload'))
    context['response'] = response

@then(parsers.parse('the response status code should be {status_code:d}'))
def check_status_code(context:dict, status_code:int):
    assert context['response'].status_code == status_code


@then(parsers.parse('the response should contain user name "{name}" and email "{email}"'))
def check_response_body(context:dict, name:str, email:str):
    data = context['response'].json()

    # Manual JSON validation
    assert "id" in data
    assert data["name"] == name
    assert data["email"] == email

    # Manual schema validation
    expected_keys = {"id", "name", "email"}
    assert set(data.keys()) == expected_keys

#Scenario 2

@given(parsers.parse('a user already exists with name "{name}" and email "{email}"'))
def give_user_already_exist(client:TestClient, name:str, email:str):
    payload = {"name":name, "email":email}
    response = client.post("/users", json=payload)
    assert response.status_code == 200 or response.status_code == 409

@when(parsers.parse('I send POST request to "{path}" with name "{name}" and email "{email}"'))
def when_sent_post_req(client:TestClient, context:dict, path:str, name:str, email:str):
    payload = {"name":name, "email":email}
    response = client.post(path, json=payload)
    context["response"] = response

@then(parsers.parse('the response status code should be {code:d}'))
def then_check_status_code(context:dict, code:int):
    res_status_code = context["response"].status_code
    assert res_status_code == code

@then(parsers.parse('the response message should be "{response_msg}"'))
def then_check_res_data(context:dict, response_msg:str):
    res_msg = context["response"].json()["detail"]
    assert res_msg == response_msg


#Scenario 3
@given(parsers.parse('a user already exists with email "{user_email}"'))
def given_user_email_already_exists(user_email:str):
    pass


#Scenario 4
@given(parsers.parse('a user exists with ID {user_id:d}'))
def given_user_id_exist(client:TestClient, user_id:int):
    user = client.get(f"/users/id/{user_id}")
    assert user.status_code == 200

@when(parsers.parse('I send GET request to "{path}"'))
def when_req_sent_by_user_id(client:TestClient, context:dict, path:str):
    response = client.get(path)
    context["response"] = response

@then(parsers.parse('the response status code should be {code:d}'))
def then_check_user_status(context:dict, code:int):
    response = context["response"]
    assert response.status_code == code

@then(parsers.parse('the response should contain user ID {user_id:d}'))
def then_check_user_res_id(context:dict, user_id:int):
    response = context["response"].json()
    assert response["id"] == user_id
