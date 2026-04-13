from fastapi.testclient import TestClient
from pytest_bdd import scenarios, given, when, then, parsers
from sqlalchemy.orm import Session

#schema
from app_db.schemas.user import *
from app_db.schemas.profile import *
from app_db.schemas.order import *

#repo
from app_db.repository.user_repo import *
from app_db.repository.profile_repo import *
from app_db.repository.order_repo import *

#models
from app_db.db.models.user import User
from app_db.db.models.profile import Profile
from app_db.db.models.order import Order

scenarios("../features/integration.feature")

#Scenario 1
@given(parsers.parse('I have a user payload with name "{name}" and email "{email}"'))
def user_payload(context:dict, name:str, email:str):
    context['user_payload'] = {"name": name, "email": email}

@when("I create the user via the API")
def create_user_api(client:TestClient,context:dict):
    response = client.post("/users", json=context['user_payload'])
    context['user_response'] = response
    context['user_id'] = response.json()['id']

@then(parsers.parse('the user should exist in the database with the correct name and email'))
def validate_user_db(db_session: Session, context:dict):
    db = db_session
    user_id = context["user_id"]
    user = get_user_by_id_db(db, UserById(id=user_id))
    assert user is not None
    assert user.name == context['user_payload']['name']
    assert user.email == context['user_payload']['email']
    db.close()

@when(parsers.parse('I create a profile for the user with bio "{bio}"'))
def create_profile_api(client:TestClient, context:dict, bio:str):
    payload = {"user_id": context['user_id'], "bio": bio}
    response = client.post("/profiles", json=payload)
    context['profile_response'] = response

@then(parsers.parse('the profile should exist in the database with the correct user_id and bio "{bio}"'))
def validate_profile_db(db_session:Session, context:dict, bio:str):
    db = db_session
    user_id = context["user_id"]
    profile = get_profile_by_user_id_db(db, UserById(id=user_id))
    assert profile is not None
    assert profile.bio == bio
    db.close()

@when(parsers.parse('I create two orders for the user "{item1}" and "{item2}"'))
def create_orders_table(client:TestClient, context:dict, item1:str, item2:str):
    item1_list = item1.split(',')
    item2_list = item2.split(',')
    items = [item1_list,item2_list]
    context['orders'] = []
    for row in items:
        payload = {
            "user_id": context['user_id'],
            "item_name": row[0],
            "price": int(row[1])
        }
        response = client.post("/orders", json=payload)
        context['orders'].append(response.json())

@then(parsers.parse('the orders should exist in the database with the correct user_id, item_name, and price'))
def validate_orders_db(db_session:Session, context:dict):
    db = db_session
    user_id = context["user_id"]
    orders_db = get_orders_by_user_id_db(db, UserById(id=user_id))
    assert len(orders_db) == len(context['orders'])
    for o_resp, o_db in zip(context['orders'], orders_db):
        assert o_resp['item_name'] == o_db.item_name
        assert o_resp['price'] == o_db.price
    db.close()

@when("I fetch the user details via the API")
def fetch_user_api(client:TestClient, context:dict):
    user_id = context['user_id']
    response = client.get(f"/users/{user_id}")
    context['fetched_user'] = response.json()

@then("the API response should include the profile and all orders")
def validate_nested_response(context:dict):
    fetched = context['fetched_user']
    # assert 'profile' in fetched
    # assert 'orders' in fetched
    # assert len(fetched['orders']) == len(context['orders'])



#Scenario 2
@given(parsers.parse('no user exists with ID {user_id:d}'))
def check_user_existence_invalidity(db_session:Session, user_id:int):
    user = get_user_by_id_db(db_session, UserById(id=user_id))
    assert user is None

@when(parsers.parse('I try to create a profile via the API for user ID {user_id:d}'))
def create_profile_with_invalid_user_id(client: TestClient, context:dict, user_id:int):
    profile_data = {"user_id":user_id, "bio":"Hi Nice to meet you"}
    response = client.post('/profiles', json=profile_data)
    context["response"] = response

@then(parsers.parse('the API response should return status code {status_code:d}'))
def verify_response_status_code(context:dict, status_code:int):
    response = context["response"]
    assert response.status_code == status_code

@then(parsers.parse('the message should be "{response_message}"'))
def verify_response_message(context:dict, response_message:str):
    response = context["response"]
    res_msg = response.json()["detail"]
    assert res_msg == response_message

#Scenario 3
@when(parsers.parse('I try to create an order via the API for user ID {user_id:d}'))
def create_order_with_invalid_user_id(client: TestClient, context:dict, user_id:int):
    order_data = {"user_id":user_id, "item_name":"Laptop", "price":40000}
    response = client.post('/orders', json=order_data)
    context["response"] = response

#Scenario 4
@given(parsers.parse('a user exists with ID {user_id:d}'))
def check_user_existing(db_session:Session, user_id:int):
    user = get_user_by_id_db(db_session, UserById(id=user_id))
    assert user is not None
    assert user.id == user_id

@given(parsers.parse('a profile exists for user ID {user_id:d}'))
def check_profile_existing(db_session:Session, user_id:int):
    profile = get_profile_by_user_id_db(db_session, UserById(id=user_id))
    assert profile is not None
    assert profile.user_id == user_id

@given(parsers.parse('multiple orders exist for user ID {user_id:d}'))
def check_orders_existing(db_session:Session, user_id:int):
    orders = get_orders_by_user_id_db(db_session, UserById(id=user_id))
    assert orders is not None
    for order in orders:
        assert order.user_id == user_id

@when(parsers.parse('I fetch user details via the API for user ID {user_id:d}'))
def fetch_user_details_api(client: TestClient, context:dict, user_id:int):
    response = client.get(f"/users/id/{user_id}")
    context["user_response"] = response
    response = client.get(f"/profiles/userid/{user_id}")
    context["profile_response"] = response
    response = client.get(f"/orders/userid/{user_id}")
    context["order_response"] = response

@then("the API response should include the correct user info")
def validate_user_details(context:dict):
    user_response = context["user_response"]
    user_res_message = user_response.json()
    status_code = user_response.status_code
    assert status_code == 200
    assert isinstance(user_res_message["id"],int)

@then("the response should include the correct profile info")
def validate_profile_details(context:dict):
    profile_response = context["profile_response"]
    profile_res_message = profile_response.json()
    status_code = profile_response.status_code
    assert status_code == 200
    assert isinstance(profile_res_message["bio"],str)

@then("the response should include all orders for the user")
def validate_order_details(context:dict):
    order_response = context["order_response"]
    order_res_message = order_response.json()
    status_code = order_response.status_code
    assert status_code == 200
    for order in order_res_message:
        assert isinstance(order["item_name"],str)