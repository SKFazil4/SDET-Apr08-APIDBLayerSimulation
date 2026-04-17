from fastapi.testclient import TestClient
from pytest_bdd import scenarios, parsers, given, when, then

scenarios("../features/profile.feature")


# -----------------------------
# COMMON HELPERS
# -----------------------------

def validate_profile_schema(data: dict):
    assert isinstance(data, dict)

    expected_keys = {"id", "user_id", "bio"}
    assert set(data.keys()) == expected_keys

    assert isinstance(data["id"], int)
    assert isinstance(data["user_id"], int)
    assert isinstance(data["bio"], str)


def validate_error_schema(data: dict):
    assert isinstance(data, dict)
    assert "detail" in data
    assert isinstance(data["detail"], str)

# -----------------------------
# SCENARIO 1: CREATE PROFILE SUCCESS
# -----------------------------

@given(parsers.parse('a user exists with ID {user_id:d}'))
def given_user_exists(client: TestClient, user_id: int):
    # Ensure user exists (create if not)
    user = client.get(f"/users/id/{user_id}")
    if not user:
        client.post("/users", json={
            "name": f"user{user_id}",
            "email": f"user{user_id}@gmail.com"
        })

@given(parsers.parse('I have a profile payload with user_id {user_id:d} and bio "{bio}"'))
def given_profile_payload(context: dict, user_id: int, bio: str):
    context["payload"] = {
        "user_id": user_id,
        "bio": bio
    }


@when(parsers.parse('I send POST request to "{path}"'))
def when_create_profile(client: TestClient, context: dict, path: str):
    response = client.post(path, json=context["payload"])
    context["response"] = response


@then(parsers.parse('the response status code should be {code:d}'))
def then_status_code(context: dict, code: int):
    assert context["response"].status_code == code


@then(parsers.parse('the response should contain user_id {user_id:d} and bio "{bio}"'))
def then_validate_profile(context: dict, user_id: int, bio: str):
    data = context["response"].json()

    # JSON validation
    assert "id" in data
    assert "user_id" in data
    assert "bio" in data

    # Schema validation
    validate_profile_schema(data)

    # Value validation
    assert data["user_id"] == user_id
    assert data["bio"] == bio


# -----------------------------
# SCENARIO 2: USER DOES NOT EXIST
# -----------------------------

@given(parsers.parse('no user exists with ID {user_id:d}'))
def given_user_not_exists(client: TestClient, user_id: int):
    response = client.get(f"/users/id/{user_id}")
    assert response.status_code == 404


@then(parsers.parse('the response message should be "{message}"'))
def then_error_message(context: dict, message: str):
    data = context["response"].json()

    # JSON validation
    assert "detail" in data

    # Schema validation
    validate_error_schema(data)

    assert data["detail"] == message


# -----------------------------
# SCENARIO 3: DUPLICATE PROFILE
# -----------------------------

@given(parsers.parse('a profile already exists for user ID {user_id:d}'))
def given_profile_exists(client: TestClient, user_id: int):
    user = client.get(f"/users/id/{user_id}")
    if not user:
        # Ensure user exists
        client.post("/users", json={
            "name": f"user{user_id}",
            "email": f"user{user_id}@gmail.com"
        })

    profile = client.get(f"/profiles/userid/{user_id}")
    if not profile:
        # Create profile
        client.post("/profiles", json={
            "user_id": user_id,
            "bio": "Initial Bio"
        })

@when(parsers.parse('I send POST request to "{path}" with user_id {user_id:d}'))
def when_duplicate_profile(client: TestClient, context: dict, path: str, user_id: int):
    response = client.post(path, json={
        "user_id": user_id,
        "bio": "Duplicate Bio"
    })
    context["response"] = response


# -----------------------------
# SCENARIO 4: GET ALL PROFILES
# -----------------------------

@given("multiple profiles exist")
def given_multiple_profiles(client: TestClient):
    for i in range(1, 3):
        client.post("/users", json={
            "name": f"user{i}",
            "email": f"user{i}@gmail.com"
        })
        client.post("/profiles", json={
            "user_id": i,
            "bio": f"Bio {i}"
        })

@when(parsers.parse('I send GET request to "{path}"'))
def when_get_profiles(client: TestClient, context: dict, path: str):
    response = client.get(path)
    context["response"] = response

@then("the response should be a list of profiles")
def then_list_profiles(context: dict):
    data = context["response"].json()

    # JSON validation
    assert isinstance(data, list)

    # Schema validation
    for profile in data:
        validate_profile_schema(profile)


# -----------------------------
# SCENARIO 5: GET PROFILE BY USER ID
# -----------------------------

@given(parsers.parse('a profile exists for user ID {user_id:d}'))
def given_profile_by_user(client: TestClient, user_id: int):
    user = client.get(f"/users/id/{user_id}")
    if not user:
        # Ensure user exists
        client.post("/users", json={
            "name": f"user{user_id}",
            "email": f"user{user_id}@gmail.com"
        })

    profile = client.get(f"/profiles/userid/{user_id}")
    if not profile:
        # Create profile
        client.post("/profiles", json={
            "user_id": user_id,
            "bio": "Initial Bio"
        })

@then(parsers.parse('the response should contain user_id {user_id:d} and bio'))
def then_profile_by_user(context: dict, user_id: int):
    data = context["response"].json()

    validate_profile_schema(data)
    assert data["user_id"] == user_id
    assert isinstance(data["bio"], str)


# -----------------------------
# SCENARIO 6: GET PROFILE FAIL
# -----------------------------


# -----------------------------
# SCENARIO 7: GET PROFILE BY PROFILE ID
# -----------------------------

@given(parsers.parse('a profile exists with profile ID {profile_id:d}'))
def given_profile_by_id(client: TestClient, profile_id: int):
    user_id = None
    user_data = client.post("/users", json={
        "name": f"user{profile_id}",
        "email": f"user{profile_id}@gmail.com"
    }).json()
    if "id" not in user_data:
        resp = client.get(f"/users/name/user{profile_id}")
        user_id = resp.json()["id"]

    actual_user_id = user_data.get("id",user_id)
    client.post("/profiles", json={
        "user_id": actual_user_id,
        "bio": "Profile Bio"
    })

@then(parsers.parse('the response should contain profile ID {profile_id:d}'))
def then_profile_id(context: dict, profile_id: int):
    data = context["response"].json()

    validate_profile_schema(data)
    assert data["id"] == profile_id


# -----------------------------
# SCENARIO 8: UPDATE PROFILE
# -----------------------------

@when(parsers.parse('I send PUT request to "{path}" with bio "{bio}"'))
def when_update_profile(client: TestClient, context: dict, path: str, bio: str):
    response = client.put(path, json={"bio": bio})
    context["response"] = response

@then(parsers.parse('the response should contain updated bio "{bio}"'))
def then_updated_profile(context: dict, bio: str):
    data = context["response"].json()

    validate_profile_schema(data)
    assert data["bio"] == bio


# -----------------------------
# SCENARIO 9: UPDATE FAIL
# -----------------------------


# -----------------------------
# SCENARIO 10: DELETE BY USER ID
# -----------------------------

@when(parsers.parse('I send DELETE request to "{path}"'))
def when_delete_profile(client: TestClient, context: dict, path: str):
    response = client.delete(path)
    context["response"] = response


# -----------------------------
# SCENARIO 11: DELETE BY PROFILE ID
# -----------------------------


# -----------------------------
# SCENARIO 12: DELETE FAIL
# -----------------------------