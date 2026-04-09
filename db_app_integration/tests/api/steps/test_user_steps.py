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
    data = context.get('response').json()

    # Manual JSON validation
    assert "id" in data
    assert data["name"] == name
    assert data["email"] == email

    # Manual schema validation
    expected_keys = {"id", "name", "email"}
    assert set(data.keys()) == expected_keys