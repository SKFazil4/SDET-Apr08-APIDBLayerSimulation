from fastapi.testclient import TestClient
from pytest_bdd import scenarios, parsers, given, when, then

scenarios("../features/orders.feature")

# -----------------------------
# COMMON HELPERS
# -----------------------------

def validate_order_schema(data: dict):
    assert isinstance(data, dict)

    expected_keys = {"id", "user_id", "item_name", "price"}
    assert set(data.keys()) == expected_keys

    assert isinstance(data["id"], int)
    assert isinstance(data["user_id"], int)
    assert isinstance(data["item_name"], str)
    assert isinstance(data["price"], int)


def validate_error_schema(data: dict):
    assert isinstance(data, dict)
    assert "detail" in data
    assert isinstance(data["detail"], str)


# -----------------------------
# SCENARIO 1: CREATE ORDER SUCCESS
# -----------------------------

@given(parsers.parse('a user exists with ID {user_id:d}'))
def given_user_exists(client: TestClient, context: dict, user_id: int):
    client.post("/users", json={
        "name": f"user{user_id}",
        "email": f"user{user_id}@gmail.com"
    })
    context["payload"] = {"user_id": user_id}

@given(parsers.parse('I have an order payload with item_name "{item_name}" and price {price:d}'))
def given_order_payload(context: dict, item_name: str, price: int):
    context["payload"].update({
        "item_name": item_name,
        "price": price
    })

@when(parsers.parse('I send POST request to "{path}"'))
def when_create_order(client: TestClient, context: dict, path: str):
    response = client.post(path, json=context["payload"])
    context["response"] = response

@then(parsers.parse('the response status code should be {code:d}'))
def then_status_code(context: dict, code: int):
    assert context["response"].status_code == code

@then(parsers.parse('the response should contain item_name "{item_name}" and price {price:d}'))
def then_validate_order(context: dict, item_name: str, price: int):
    data = context["response"].json()

    # JSON validation
    assert "id" in data
    assert "user_id" in data
    assert "item_name" in data
    assert "price" in data

    # Schema validation
    validate_order_schema(data)

    # Value validation
    assert data["item_name"] == item_name
    assert data["price"] == price

@then(parsers.parse('the response should contain user_id {user_id:d}'))
def then_validate_user_id(context: dict, user_id: int):
    data = context["response"].json()

    assert data["user_id"] == user_id


# -----------------------------
# SCENARIO 2: USER DOES NOT EXIST
# -----------------------------

@given(parsers.parse('no user exists with ID {user_id:d}'))
def given_user_not_exists(context: dict, user_id: int):
    context["payload"] = {"user_id": user_id}

@then(parsers.parse('the response message should be "{message}"'))
def then_error_message(context: dict, message: str):
    data = context["response"].json()

    # JSON validation
    assert "detail" in data

    # Schema validation
    validate_error_schema(data)

    assert data["detail"] == message


# -----------------------------
# SCENARIO 3: GET ALL ORDERS
# -----------------------------

@given("multiple orders exist")
def given_multiple_orders(client: TestClient):
    for i in range(1, 3):
        client.post("/users", json={
            "name": f"user{i}",
            "email": f"user{i}@gmail.com"
        })
        client.post("/orders", json={
            "user_id": i,
            "item_name": f"Item{i}",
            "price": i * 100
        })

@when(parsers.parse('I send GET request to "{path}"'))
def when_get_orders(client: TestClient, context: dict, path: str):
    response = client.get(path)
    context["response"] = response

@then("the response should be a list of orders")
def then_list_orders(context: dict):
    data = context["response"].json()

    # JSON validation
    assert isinstance(data, list)

    # Schema validation
    for order in data:
        validate_order_schema(order)


# -----------------------------
# SCENARIO 4: GET ORDERS BY USER ID
# -----------------------------

@given(parsers.parse('multiple orders exist for user ID {user_id:d}'))
def given_orders_for_user(client: TestClient, user_id: int):
    client.post("/users", json={
        "name": f"user{user_id}",
        "email": f"user{user_id}@gmail.com"
    })

    for i in range(2):
        client.post("/orders", json={
            "user_id": user_id,
            "item_name": f"Item{i}",
            "price": 100
        })

@then(parsers.parse('all returned orders should contain user_id {user_id:d}'))
def then_orders_by_user(context: dict, user_id: int):
    data = context["response"].json()
    for order in data:
        validate_order_schema(order)
        assert order["user_id"] == user_id


# -----------------------------
# SCENARIO 5: GET FAIL
# -----------------------------


# -----------------------------
# SCENARIO 6: GET ORDER BY ID
# -----------------------------

@given(parsers.parse('an order exists with ID {order_id:d}'))
def given_order_exists(client: TestClient, order_id: int):
    client.post("/users", json={
        "name": f"user{order_id}",
        "email": f"user{order_id}@gmail.com"
    })

    client.post("/orders", json={
        "user_id": order_id,
        "item_name": "Sample",
        "price": 100
    })

@then(parsers.parse('the response should contain order ID {order_id:d}'))
def then_order_id(context: dict, order_id: int):
    data = context["response"].json()

    validate_order_schema(data)
    assert data["id"] == order_id


# -----------------------------
# SCENARIO 7: UPDATE ORDER
# -----------------------------

@when(parsers.parse('I send PUT request to "{path}" with item_name "{item_name}" and price {price:d}'))
def when_update_order(client: TestClient, context: dict, path: str, item_name: str, price: int):
    response = client.put(path, json={
        "user_id": 1,
        "item_name": item_name,
        "price": price
    })
    context["response"] = response

@then(parsers.parse('the response should contain updated item_name "{item_name}" and price {price:d}'))
def then_updated_order(context: dict, item_name: str, price: int):
    data = context["response"].json()

    validate_order_schema(data)
    assert data["item_name"] == item_name
    assert data["price"] == price

# -----------------------------
# SCENARIO 8: UPDATE FAIL
# -----------------------------


# -----------------------------
# SCENARIO 9, 10 & 11: DELETE
# -----------------------------

@when(parsers.parse('I send DELETE request to "{path}"'))
def when_delete_order(client: TestClient, context: dict, path: str):
    response = client.delete(path)
    context["response"] = response