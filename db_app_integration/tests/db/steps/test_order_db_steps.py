from pytest_bdd import given, when, then, parsers, scenarios

from app_db.db.models.order import Order
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

#Repository
from app_db.repository.user_repo import get_user_by_id
from app_db.repository.profile_repo import *
from app_db.repository.order_repo import *

#Schemas
from app_db.schemas.user import UserWithRelations


scenarios("../features/orders.feature")

@given(parsers.parse('a user exists with ID {user_id:d}'))
def given_user_exists(context:dict, user_id:int):
    context["payload"] = {"user_id":user_id}

@given(parsers.parse('I have an order payload with item_name "{name}" and price {price:d}'))
def given_order_payload(context:dict, name:str, price:int):
    context["payload"].update({"item_name":name,"price":price})

@when("I insert the order into the orders table")
def when_order_inserted(db_session:Session, context:dict):
    payload = context["payload"]
    order_create = OrderCreate(user_id=payload["user_id"], item_name=payload["item_name"], price=payload["price"])
    order = create_order_for_user_db(db_session, order_create)
    context["order"] = order

@then("the order should exist with the correct item_name, price, and user_id")
def then_order_details_should_exist(context:dict):
    payload = context["payload"]
    order = context["order"]
    assert order is not None
    assert payload["user_id"] == order.user_id
    assert payload["item_name"] == order.item_name
    assert payload["price"] == order.price

@given(parsers.parse('no user exists with ID {user_id:d}'))
def given_non_existing_user_id(user_id:int):
    pass

@when(parsers.parse('I try to insert an order with user_id {user_id:d}'))
def when_try_to_insert_order(db_session, context:dict, user_id:int):
    try:
        order_create = OrderCreate(user_id=user_id, item_name="mobile", price=100)
        order = create_order_for_user_db(db_session, order_create)
        context["order"] = order
    except IntegrityError as e:
        context["error"] = e
    else:
        context["error"] = None

@then("the database should raise a foreign key constraint error")
def then_verify_foreign_key_error(context:dict):
    error = context["error"]
    assert error is not None
    assert isinstance(error,IntegrityError)

@given(parsers.parse('multiple orders exist for user ID {user_id:d}'))
def given_multi_orders(user_id:int):
    pass

@when(parsers.parse('I query the orders table for user ID {user_id:d}'))
def when_query_user_orders(db_session:Session, context:dict, user_id:int):
    orders = get_orders_by_user_id(db_session, UserById(id=user_id))
    context["orders"] = orders

@then("all orders should be returned correctly")
def then_verify_all_orders_exist(context:dict):
    orders = context["orders"]
    assert orders is not  None
    assert len(orders) > 0
    for order in orders:
        assert isinstance(order.user_id, int)
        assert isinstance(order.item_name, str)
        assert isinstance(order.price, int)