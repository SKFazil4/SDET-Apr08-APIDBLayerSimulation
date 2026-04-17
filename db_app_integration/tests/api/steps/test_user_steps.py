from fastapi.testclient import TestClient
from pytest_bdd import scenarios, parsers, given, when, then

scenarios("../features/users.feature")

# -----------------------------
# COMMON HELPERS
# -----------------------------

def validate_user_schema(data: dict):
    assert isinstance(data, dict)

    expected_keys = {"id", "name", "email"}
    assert set(data.keys()) == expected_keys

    assert isinstance(data["id"], int)
    assert isinstance(data["name"], str)
    assert isinstance(data["email"], str)

def validate_error_schema(data: dict):
    assert isinstance(data, dict)
    assert "detail" in data
    assert isinstance(data["detail"], str)

# -----------------------------
# SCENARIO 1: CREATE USER SUCCESS
# -----------------------------
@given(parsers.parse('I have a user payload with name "{name}" and email "{email}"'))
def given_user_payload(context: dict, name: str, email: str):
    context["payload"] = {"name": name, "email": email}

@when(parsers.parse('I send POST request to "{path}"'))
def when_create_user(client: TestClient, context: dict, path: str):
    response = client.post(path, json=context["payload"])
    context["response"] = response

@then(parsers.parse('the response status code should be {code:d}'))
def then_status_code(context: dict, code: int):
    assert context["response"].status_code == code

@then(parsers.parse('the response should contain user name "{name}" and email "{email}"'))
def then_validate_user(context: dict, name: str, email: str):
    data = context["response"].json()

    # JSON validation
    assert "id" in data
    assert "name" in data
    assert "email" in data

    # Schema validation
    validate_user_schema(data)

    # Value validation
    assert data["name"] == name
    assert data["email"] == email

@then("the response should contain a valid user ID")
def then_validate_user_id(context: dict):
    data = context["response"].json()

    assert isinstance(data["id"], int)
    assert data["id"] > 0


# -----------------------------
# SCENARIO 2: DUPLICATE NAME
# -----------------------------

@given(parsers.parse('a user already exists with name "{name}" and email "{email}"'))
def given_existing_user_name(client: TestClient, name: str, email: str):
    client.post("/users", json={"name": name, "email": email})

@when(parsers.parse('I send POST request to "{path}" with name "{name}" and email "{email}"'))
def when_post_duplicate(client: TestClient, context: dict, path: str, name: str, email: str):
    response = client.post(path, json={"name": name, "email": email})
    context["response"] = response

@then(parsers.parse('the response message should be "{msg}"'))
def then_error_message(context: dict, msg: str):
    data = context["response"].json()

    # JSON validation
    assert "detail" in data

    # Schema validation
    validate_error_schema(data)

    assert data["detail"] == msg


# -----------------------------
# SCENARIO 3: DUPLICATE EMAIL
# -----------------------------

@given(parsers.parse('a user already exists with email "{email}"'))
def given_existing_email(client: TestClient, email: str):
    user_name = email.split('@')[0].strip()
    client.post("/users", json={"name": user_name, "email": email})


# -----------------------------
# SCENARIO 4: GET ALL USERS
# -----------------------------

@given("multiple users exist")
def given_multiple_users(client: TestClient):
    users = [
        {"name": "User1", "email": "user1@gmail.com"},
        {"name": "User2", "email": "user2@gmail.com"},
    ]
    for u in users:
        client.post("/users", json=u)

@when(parsers.parse('I send GET request to "{path}"'))
def when_get_request(client: TestClient, context: dict, path: str):
    response = client.get(path)
    context["response"] = response

@then("the response should be a list of users")
def then_list_users(context: dict):
    data = context["response"].json()
    # JSON validation
    assert isinstance(data, list)

    # Schema validation
    for user in data:
        validate_user_schema(user)


# -----------------------------
# SCENARIO 5: GET USER BY ID
# -----------------------------

@given(parsers.parse('a user exists with ID {user_id:d}'))
def given_user_id(client: TestClient, user_id: int):
    # ensure at least one user exists
    client.post("/users", json={"name": f"user{user_id}", "email": f"user{user_id}@test.com"})

@then(parsers.parse('the response should contain user ID {user_id:d}'))
def then_check_user_id(context: dict, user_id: int):
    data = context["response"].json()
    validate_user_schema(data)
    assert data["id"] == user_id

@then("the response should contain name and email")
def then_check_name_email(context: dict):
    data = context["response"].json()
    validate_user_schema(data)

# -----------------------------
# SCENARIO 6: INVALID USER ID
# -----------------------------
# uses same GET + status + error steps

# -----------------------------
# SCENARIO 7: GET BY NAME
# -----------------------------

@given(parsers.parse('a user exists with name "{name}"'))
def given_user_name(client: TestClient, name: str):
    client.post("/users", json={"name": name, "email": f"{name}@gmail.com"})

@then(parsers.parse('the response should contain user name "{name}"'))
def then_check_name(context: dict, name: str):
    data = context["response"].json()

    validate_user_schema(data)
    assert data["name"] == name


# -----------------------------
# SCENARIO 8: GET BY EMAIL
# -----------------------------

@given(parsers.parse('a user exists with email "{email}"'))
def given_user_email(client: TestClient, email: str):
    user_name = email.split('@')[0].strip()
    client.post("/users", json={"name": user_name, "email": email})

@then(parsers.parse('the response should contain email "{email}"'))
def then_check_email(context: dict, email: str):
    data = context["response"].json()

    validate_user_schema(data)
    assert data["email"] == email


# -----------------------------
# SCENARIO 9: UPDATE USER
# -----------------------------

@when(parsers.parse('I send PUT request to "{path}" with name "{name}" and email "{email}"'))
def when_put_request(client: TestClient, context: dict, path: str, name: str, email: str):
    response = client.put(path, json={"name": name, "email": email})
    context["response"] = response

@then(parsers.parse('the response should contain updated name "{name}" and email "{email}"'))
def then_updated_user(context: dict, name: str, email: str):
    data = context["response"].json()

    validate_user_schema(data)
    assert data["name"] == name
    assert data["email"] == email

# -----------------------------
# SCENARIO 10: UPDATE FAIL
# -----------------------------
# uses same PUT + status


# -----------------------------
# SCENARIO 11: DELETE USER
# -----------------------------

@when(parsers.parse('I send DELETE request to "{path}"'))
def when_delete_request(client: TestClient, context: dict, path: str):
    response = client.delete(path)
    context["response"] = response

@then("the response message should confirm deletion")
def then_delete_msg(context: dict):
    data = context["response"].json()

    # JSON validation
    assert "response" in data

    # Schema validation
    assert isinstance(data["response"], str)

    assert "deleted" in data["response"].lower()

# -----------------------------
# SCENARIO 12: DELETE FAIL
# -----------------------------
# uses same DELETE + status