from fastapi.testclient import TestClient
from pytest_bdd import scenarios, given, when, then, parsers

from sqlalchemy.orm import Session
import json

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


#CREATE + FULL FLOW
# Scenario 1
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
    context["profile_payload"] = {"user_id": context['user_id'], "bio": bio}
    response = client.post("/profiles", json=context["profile_payload"])
    context['profile_response'] = response

@then(parsers.parse('the profile should exist in the database with the correct user_id and bio'))
def validate_profile_db(db_session:Session, context:dict):
    db = db_session
    bio = context["profile_payload"]["bio"]
    user_id = context["user_id"]
    profile = get_profile_by_user_id_db(db, UserById(id=user_id))
    assert profile is not None
    assert profile.bio == bio
    db.close()

@when(parsers.parse('I create two orders for the user "{orders}"'))
def create_orders_table(client:TestClient, context:dict, orders:str):
    orders = json.loads(orders)
    context['orders'] = []
    for order in orders:
        payload = {
            "user_id": context['user_id'],
            "item_name": order['item'],
            "price": order['price']
        }
        response = client.post("/orders", json=payload)
        context['orders'].append(response.json())

@then("the orders should exist in the database with correct details")
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
    user_response = client.get(f"/users/id/{user_id}")
    profile_response = client.get(f"/profiles/userid/{user_id}")
    order_response = client.get(f"/orders/userid/{user_id}")
    details = {
        "user":user_response.json(),
        "profile":profile_response.json(),
        "orders":order_response.json()
    }
    context['fetched_user'] = details

@then("the API response should include correct user info")
def validate_nested_response(context:dict):
    fetched = context['fetched_user']
    assert 'profile' in fetched
    assert 'orders' in fetched
    assert len(fetched['orders']) == len(context['orders'])


#USER APIs
#Scenario 1
@given("multiple users exist")
def given_multiple_users_exist(db_session:Session):
    users = get_user_details_db(db_session)
    assert len(users) > 1

@when("I fetch all users via the API")
def when_all_users_fetched_via_api(context:dict, client:TestClient):
    response = client.get("/users")
    context['users_response'] = response.json()

@then("the API response should return all users")
def then_api_response_should_have_all_users(context:dict):
    users_response = context['users_response']
    assert len(users_response)

@then("the database should contain the same number of users")
def then_check_number_of_users_in_db(db_session:Session,context:dict):
    users = get_user_details_db(db_session)
    users_response = context['users_response']
    assert len(users) == len(users_response)

#USER APIs
#Scenario 2
@given(parsers.parse('a user exists with name "{name}" and email "{mail}"'))
def given_user_exists(client:TestClient, context:dict, name:str, mail:str):
    payload = {"name":name,"email":mail}
    response = client.post('/users', json=payload)
    context["user_response"] = response.json()

@when(parsers.parse('I fetch user by name "{name}"'))
def when_fetch_user_by_name(db_session:Session, context:dict, name:str):
    user = get_user_by_name_db(db_session,UserByName(name=name))
    assert user is not None
    context["user_db_res"] = user

@then("the API response of user should match the database record")
def then_api_res_user_match_db_record(context:dict):
    user_api_res = context["user_response"]
    user_db_res = context["user_db_res"]
    assert user_api_res["id"] == user_db_res.id
    assert user_api_res["name"] == user_db_res.name
    assert user_api_res["email"] == user_db_res.email

@when(parsers.parse('I fetch user by email "{mail}"'))
def when_fetch_user_by_email(db_session:Session, context:dict, mail:str):
    user = get_user_by_mail_db(db_session, UserByEmail(email=mail))
    assert user is not None
    context["user_db_res"] = user

#USER APIs
#Scenario 3
@given(parsers.parse('a user exists with ID {user_id:d}'))
def given_user_exists_by_id(db_session:Session, context:dict, user_id:int):
    user = get_user_by_id_db(db_session, UserById(id=user_id))
    assert user is not None
    assert user.id == user_id
    context["user_id"] = user_id

@when(parsers.parse('I update the user with name "{name}" and email "{mail}"'))
def when_updating_user(client:TestClient, context:dict, name:str, mail:str):
    user_id = context["user_id"]
    context["user_payload"] = {"name":name, "email":mail}
    response = client.put(f"/users/id/{user_id}", json=context["user_payload"])
    context["user_response"] = response.json()

@then("the API response should reflect updated values")
def then_api_should_reflect_updated_values(context:dict):
    user_response = context["user_response"]
    payload = context["user_payload"]
    assert payload["name"] == user_response["name"]
    assert payload["email"] == user_response["email"]

@then("the database should reflect updated values")
def then_db_should_reflect_updated_values(db_session:Session, context:dict):
    user_id = context["user_id"]
    user_response = get_user_by_id_db(db_session, UserById(id=user_id))
    assert user_response is not None
    payload = context["user_payload"]
    assert payload["name"] == user_response.name
    assert payload["email"] == user_response.email

#USER APIs
#Scenario 4
@given(parsers.parse('{no_of_users:d} users exist'))
def given_users_exist(db_session:Session, no_of_users:int):
    users = get_user_details_db(db_session)
    assert len(users) == no_of_users

@when(parsers.parse('I try to update one user Id {user_id:d} with duplicate name "{name}" or email "{email}"'))
def when_try_to_update_user_by_duplicates(client:TestClient, db_session:Session, context:dict, user_id:int, name:str, email:str):
    context["user_id"] = user_id
    payload = {"name":name,"email":email}
    context["user_payload"] = payload
    context["old_db_data"] = get_user_by_id_db(db_session, UserById(id=user_id))
    user_res = client.put(f"/users/id/{user_id}", json=payload)
    context["user_res"] = user_res

@then("the API should return appropriate error")
def then_check_api_error_for_dupli_user_update(context:dict):
    payload = context["user_payload"]
    user_res = context["user_res"]
    assert user_res.status_code == 401
    assert user_res.json()["detail"] in (f"Duplicate username {payload.get("name")}", f"Duplicate user email {payload.get("email")}")

@then("the database should remain unchanged")
def then_db_must_be_unchanged(db_session:Session, context:dict):
    db_data = context["old_db_data"]
    user_id =  context["user_id"]
    existing_data = get_user_by_id_db(db_session, UserById(id=user_id))
    assert db_data.name == existing_data.name
    assert db_data.email == existing_data.email


#PROFILE APIs
#Scenario 1
@given("multiple profiles exist")
def given_multiple_profiles_exist(db_session):
    profiles = get_profile_details_db(db_session)
    assert len(profiles) > 1

@when("I fetch all profiles via the API")
def when_profiles_fetch_via_api(client:TestClient, context:dict):
    profiles = client.get("/profiles")
    context["profiles_res"] = profiles.json()

@then("the API response should return all profiles")
def then_api_res_should_return_all_profiles(context:dict):
    profiles = context["profiles_res"]
    assert len(profiles) > 1

@then("the database should match the response")
def then_db_should_match_res(db_session:Session, context:dict):
    profiles_api = context["profiles_res"]
    profiles_db = get_profile_details_db(db_session)
    assert len(profiles_api) == len(profiles_db)


#PROFILE APIs, DELETE OPERATIONS
#Scenario 2
@given(parsers.parse('a profile exists with profile ID {profile_id:d}'))
def given_profile_exist(db_session:Session, context:dict, profile_id:int):
    profile = get_profile_by_profile_id_db(db_session, ProfileById(id=profile_id))
    assert profile is not None
    context["profile_db"] = profile
    context["profile_id"] = profile_id
@when("I fetch the profile via the API using profile ID")
def when_fetch_profile_using_profile_id_by_api(client:TestClient, context:dict):
    profile_id = context["profile_id"]
    profile = client.get(f"/profiles/profileid/{profile_id}")
    context["profile_res"] = profile.json()
@then("the API response of profile should match the database record")
def then_api_res_profile_match_db_record(context:dict):
    profile_db = context["profile_db"]
    profile_api = context["profile_res"]
    assert profile_db.id == profile_api["id"]
    assert profile_db.user_id == profile_api["user_id"]
    assert profile_db.bio == profile_api["bio"]


#PROFILE APIs
#Scenario 3
@given(parsers.parse('a profile exists for user ID {user_id:d}'))
def given_profile_exist_by_user_id(db_session:Session, context:dict, user_id:int):
    profile = get_profile_by_user_id_db(db_session, UserById(id=user_id))
    assert profile is not None
    context["user_id"] = user_id
@when(parsers.parse('I update the profile bio to "{bio}"'))
def when_profile_bio_updating(client:TestClient, context:dict, bio:str):
    user_id = context["user_id"]
    payload = {"user_id":user_id, "bio":bio}
    context["profile_payload"] = payload
    profile = client.put(f"/profiles/id/{user_id}", json=payload)
    context["profile_res"] = profile.json()
@then("the API response should reflect updated bio")
def then_check_updated_bio_in_api_response(context:dict):
    payload = context["profile_payload"]
    profile_res = context["profile_res"]
    assert payload["user_id"] == profile_res["user_id"]
    assert payload["bio"] == profile_res["bio"]
@then("the database should reflect updated bio")
def then_db_should_reflect_updated_bio(db_session:Session, context:dict):
    user_id = context["user_id"]
    payload = context["profile_payload"]
    profile_db = get_profile_by_user_id_db(db_session, UserById(id = user_id))
    assert payload["user_id"] == profile_db.user_id
    assert payload["bio"] == profile_db.bio


#ORDER APIs
#Scenario 1
@given("multiple orders exist")
def given_multiple_orders_exists(db_session:Session, context:dict):
    orders = get_orders_db(db_session)
    assert orders is not None
    context["orders_db"] = orders
@when("I fetch all orders via the API")
def when_all_orders_fetch_via_api(client:TestClient, context:dict):
    orders = client.get("/orders")
    assert orders is not None
    context["orders_res"] = orders.json()
@then("the API response should return all orders")
def then_check_returned_orders_by_api(context:dict):
    orders = context["orders_res"]
    assert len(orders) > 1
@then("the database should match the response")
def then_db_should_match_api_res(context:dict):
    orders_db = context["orders_db"]
    orders_res = context["orders_res"]
    assert len(orders_res) == len(orders_db)
    for order_res, order_db in zip(orders_res, orders_db):
        assert order_res["id"] == order_db.id
        assert order_res["user_id"] == order_db.user_id
        assert order_res["item_name"] == order_db.item_name
        assert order_res["price"] == order_db.price


#ORDER APIs
#Scenario 2
#Scenario 3
@given(parsers.parse('an order exists with ID {order_id:d}'))
def given_order_exist_by_order_id(db_session:Session, context:dict, order_id:int):
    order = get_order_by_order_id_db(db_session, OrderById(id=order_id))
    assert order is not None
    context["order_db"] = order
    context["order_id"] = order_id
@when("I fetch the order via the API")
def when_order_fetch_via_api(client:TestClient, context:dict):
    order_id = context["order_id"]
    order = client.get(f"/orders/orderid/{order_id}")
    order = order.json()
    assert order is not None
    context["order_res"] = order
@then("the API response of order should match the database record")
def then_api_res_order_match_db_record(context:dict):
    order_db = context["order_db"]
    order_res = context["order_res"]
    assert order_db.id == order_res["id"]
    assert order_db.user_id == order_res["user_id"]
    assert order_db.item_name == order_res["item_name"]
    assert order_db.price == order_res["price"]


#ORDER APIs
#Scenario 3
@when(parsers.parse('I update the order with item "{item}" and price {price:d}'))
def when_order_updating(client:TestClient, context:dict, item:str, price:int):
    order_id = context["order_id"]
    order_db = context["order_db"]
    payload = {"user_id":order_db.user_id, "item_name":item, "price":price}
    context["order_payload"] = payload
    order = client.put(f"/orders/id/{order_id}", json=payload)
    order = order.json()
    assert order is not None
    context["order_res"] = order

@then("the API response should reflect updated order")
def then_api_res_reflect_updated_order(context:dict):
    order_api = context["order_res"]
    payload = context["order_payload"]
    assert order_api["user_id"] == payload["user_id"]
    assert order_api["item_name"] == payload["item_name"]
    assert order_api["price"] == payload["price"]

@then("the database should reflect updated order")
def then_db_reflect_updated_order(db_session:Session, context:dict):
    db_session.expire_all()
    payload = context["order_payload"]
    order_id = context["order_id"]
    existing_order = get_order_by_order_id_db(db_session, OrderById(id=order_id))
    assert existing_order.user_id == payload["user_id"]
    assert existing_order.item_name == payload["item_name"]
    assert existing_order.price == payload["price"]


#DELETE OPERATIONS
#Scenario 1
@when("I delete the profile using profile ID via API")
def when_profile_deleted_by_profile_id_by_api(context:dict, client:TestClient):
    profile_id = context["profile_id"]
    response = client.delete(f"/profiles/profileid/{profile_id}")
    assert response.json()["response"] == f"Profile with profile Id {profile_id} has been deleted successfully"
@then("the profile should not exist in the database")
def then_profile_should_not_exist_in_db(db_session:Session, context:dict):
    db_session.expire_all()
    profile_id = context["profile_id"]
    profile_db_res = get_profile_by_profile_id_db(db_session, ProfileById(id=profile_id))
    assert profile_db_res is None


#DELETE OPERATIONS
#Scenario 2
@when("I delete the order via API")
def when_order_deleted_by_order_id_via_api(client:TestClient, context:dict):
    order_id = context["order_id"]
    response = client.delete(f"/orders/orderid/{order_id}")
    assert response.json()["response"] == f"Order with user Id {order_id} has been deleted successfully"
@then("the order should not exist in the database")
def then_order_should_not_exist_in_db(db_session:Session, context:dict):
    db_session.expire_all()
    order_id = context["order_id"]
    order_res_db = get_order_by_order_id_db(db_session, OrderById(id=order_id))
    assert order_res_db is None


#DELETE OPERATIONS
#Scenario 2
@given(parsers.parse('a user exists with name "{name}"'))
def given_user_exists_by_name(db_session:Session, context:dict, name:str):
    user_res_db = get_user_by_name_db(db_session, UserByName(name=name))
    assert user_res_db is not None
    context["user_name"] = name
@when("I delete the user using name via API")
def when_user_deleted_using_name_via_api(client:TestClient, context:dict):
    user_name = context["user_name"]
    user_res = client.delete(f"/users/name/{user_name}")
    assert f"User {user_name} has been deleted successfully"
@then("the user should not exist in the database")
def then_user_should_not_exist_in_db(db_session:Session, context:dict):
    db_session.expire_all()
    user_name = context["user_name"]
    user_db_res = get_user_by_name_db(db_session, UserByName(name=user_name))
    assert user_db_res is None

#CASCADE VALIDATION (CRITICAL)
@given(parsers.parse('a user exists with ID {user_id:d} and with profile and orders'))
def given_user_exist_with_id_and_with_its_profile_order(db_session:Session, context:dict, user_id:int):
    context["user_id"]=user_id
    user_res = get_user_by_id_db(db_session, UserById(id = user_id))
    assert user_res is not None
    context["user_name"] = user_res.name
    profile_res = get_profile_by_user_id_db(db_session, UserById(id = user_id))
    assert profile_res is not None
    context["profile_id"] = profile_res.id
    orders_res = get_orders_by_user_id_db(db_session, UserById(id = user_id))
    assert orders_res is not None
@when("I delete the user via the API")
def when_user_deleted_by_user_id_via_api(client:TestClient, context:dict):
    user_id = context["user_id"]
    user_res = client.delete(f"/users/id/{user_id}")
    assert user_res.json()["response"] == f"User {user_id} has been deleted successfully"
@then("the orders should not exist in the database")
def then_orders_should_not_exist_in_db(db_session:Session, context:dict):
    db_session.expire_all()
    user_id = context["user_id"]
    order_res_db = get_orders_by_user_id_db(db_session, UserById(id=user_id))
    assert len(order_res_db) == 0


#NEGATIVE CASES
#Scenario 1
@given(parsers.parse('no user exists with ID {user_id:d}'))
def given_no_user_exist(db_session:Session, context:dict, user_id:int):
    user = get_user_by_id_db(db_session, UserById(id = user_id))
    assert user is None
    context["user_id"] = user_id
@when("I try to create a profile")
def when_try_to_create_profile(client:TestClient, context:dict):
    user_id = context["user_id"]
    payload = {"user_id":user_id, "bio":"Hi I'm good how about you"}
    profile_res = client.post(f"/profiles", json=payload)
    context["api_res"] = profile_res
@then(parsers.parse('the API response should return status code {code:d}'))
def then_verify_api_res_returns_status_code(context:dict, code:int):
    api_res = context["api_res"]
    assert api_res.status_code == code


#NEGATIVE CASES
#Scenario 2
@when("I try to create an order")
def when_try_to_create_profile(client:TestClient, context:dict):
    user_id = context["user_id"]
    payload = {"user_id":user_id, "item_name":"Laptop", "price":55000}
    order_res = client.post(f"/orders", json=payload)
    context["api_res"] = order_res


#NEGATIVE CASES
#Scenario 3
@when("I fetch user/profile/order with invalid IDs")
def when_using_invalid_user_id_details_fetched(client:TestClient, context:dict):
    user_id = 9999
    user_res = client.get(f"/users/id/{user_id}")
    profile_res = client.get(f"/profiles/userid/{user_id}")
    order_res = client.get(f"/orders/userid/{user_id}")
    context["user_res"] = user_res
    context["profile_res"] = profile_res
    context["order_res"] = order_res
@then(parsers.parse('the API should return {code:d} responses'))
def then_api_should_return_status_code(context:dict):
    user_res = context["user_res"]
    profile_res = context["profile_res"]
    order_res = context["order_res"]
    assert user_res.status_code == 404
    assert profile_res.status_code == 404
    assert order_res.status_code == 404

#CONSISTENCY VALIDATION
@when("I fetch user, profile, and orders via APIs")
def when_user_profile_order_were_fetch_via_api(client:TestClient, context:dict):
    user_id = context["user_id"]
    user_api_res = client.get(f"/users/id/{user_id}")
    assert user_api_res.status_code == 200
    profile_api_res = client.get(f"/profiles/userid/{user_id}")
    assert profile_api_res.status_code == 200
    orders_api_res = client.get(f"/orders/userid/{user_id}")
    assert orders_api_res.status_code == 200

    context["user_api_res"] = user_api_res
    context["profile_api_res"] = profile_api_res
    context["orders_api_res"] = orders_api_res
@then("all responses should match database records")
def then_check_responses_should_match_db(db_session:Session, context:dict):
    user_id = context["user_id"]

    user_api_res = context["user_api_res"]
    user_api = user_api_res.json()

    profile_api_res = context["profile_api_res"]
    profile_api = profile_api_res.json()

    orders_api_res = context["orders_api_res"]
    orders_api = orders_api_res.json()

    user_db_res = get_user_by_id_db(db_session, UserById(id=user_id))
    assert user_db_res.id == user_api["id"]
    assert user_db_res.name == user_api["name"]
    assert user_db_res.email == user_api["email"]

    profile_db_res = get_profile_by_user_id_db(db_session, UserById(id=user_id))
    assert profile_db_res.id == profile_api["id"]
    assert profile_db_res.user_id == profile_api["user_id"]
    assert profile_db_res.bio == profile_api["bio"]

    orders_db_res = get_orders_by_user_id_db(db_session, UserById(id=user_id))
    assert len(orders_db_res) == len(orders_api)
    for order_db, order_api in zip(orders_db_res, orders_api):
        assert order_db.id == order_api["id"]
        assert order_db.user_id == order_api["user_id"]
        assert order_db.item_name == order_api["item_name"]
        assert order_db.price == order_api["price"]


#EMPTY DATA EDGE CASES
@given("no users, profiles, or orders exist")
def given_no_user_profile_order_exist(db_session:Session):
    user_res = get_user_details_db(db_session)
    assert len(user_res) == 0
    profile_res = get_profile_details_db(db_session)
    assert len(profile_res) == 0
    order_res = get_orders_db(db_session)
    assert len(order_res) == 0

@when("I fetch all users, profiles, and orders")
def when_fetch_all_users_profiles_orders(client:TestClient, context:dict):
    user_res = client.get("/users")
    profile_res = client.get("/profiles")
    order_res = client.get("/orders")
    context["user_res"] = user_res
    context["profile_res"] = profile_res
    context["order_res"] = order_res
@then("the API should return appropriate responses or errors")
def then_api_should_return_appropriate_res_or_error(context:dict):
    user_res = context["user_res"]
    profile_res= context["profile_res"]
    order_res = context["order_res"]

    assert user_res.status_code == 404
    assert user_res.json()["detail"] == "Users does not exists"
    assert profile_res.status_code == 404
    assert profile_res.json()["detail"] == "Profiles does not exists"
    assert order_res.status_code == 404
    assert order_res.json()["detail"] == "orders does not exist"