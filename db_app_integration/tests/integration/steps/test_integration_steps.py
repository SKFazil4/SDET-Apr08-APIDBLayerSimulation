from pytest_bdd import scenarios, given, when, then, parsers
from app_db.db.session import SessionLocal
from app_db.db.models.user import User
from app_db.db.models.profile import Profile
from app_db.db.models.order import Order

scenarios("../features/integration.feature")

@given(parsers.parse('I have a user payload with name "{name}" and email "{email}"'))
def user_payload(context, name, email):
    context['user_payload'] = {"name": name, "email": email}

@when("I create the user via the API")
def create_user_api(client,context):
    response = client.post("/users", json=context['user_payload'])
    context['user_response'] = response
    context['user_id'] = response.json()['id']

@then(parsers.parse('the user should exist in the database with the correct name and email'))
def validate_user_db(db_session, context):
    db = db_session
    user = db.query(User).filter(User.id == context['user_id']).first()
    assert user is not None
    assert user.name == context['user_payload']['name']
    assert user.email == context['user_payload']['email']
    db.close()

@when(parsers.parse('I create a profile for the user with bio "{bio}"'))
def create_profile_api(client, context, bio):
    payload = {"user_id": context['user_id'], "bio": bio}
    response = client.post("/profiles", json=payload)
    context['profile_response'] = response

@then(parsers.parse('the profile should exist in the database with the correct user_id and bio'))
def validate_profile_db(context, bio):
    db = SessionLocal()
    profile = db.query(Profile).filter(Profile.user_id == context['user_id']).first()
    assert profile is not None
    assert profile.bio == bio
    db.close()

@when(parsers.parse('I create orders for the user:'))
def create_orders_table(client, context, table):
    """
    table is a list of dicts: [{'item_name': 'Laptop', 'price': '1200'}, ...]
    """
    context['orders'] = []
    for row in table:
        payload = {
            "user_id": context['user_id'],
            "item_name": row['item_name'],
            "price": int(row['price'])
        }
        response = client.post("/orders", json=payload)
        context['orders'].append(response.json())

@then(parsers.parse('the orders should exist in the database with the correct user_id, item_name, and price'))
def validate_orders_db(context):
    db = SessionLocal()
    orders_db = db.query(Order).filter(Order.user_id == context['user_id']).all()
    assert len(orders_db) == len(context['orders'])
    for o_resp, o_db in zip(context['orders'], orders_db):
        assert o_resp['item_name'] == o_db.item_name
        assert o_resp['price'] == o_db.price
    db.close()

@when("I fetch the user details via the API")
def fetch_user_api(client, context):
    user_id = context['user_id']
    response = client.get(f"/users/{user_id}")
    context['fetched_user'] = response.json()

@then("the API response should include the profile and all orders")
def validate_nested_response(context):
    fetched = context['fetched_user']
    assert 'profile' in fetched
    assert 'orders' in fetched
    assert len(fetched['orders']) == len(context['orders'])