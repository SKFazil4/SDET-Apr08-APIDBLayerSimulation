from pytest_bdd import given, when, then, parsers, scenarios
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

#Repository
from app_db.repository.profile_repo import *
from app_db.repository.order_repo import *
from app_db.repository.user_repo import *

#Model
from app_db.db.models.order import Order

#Schema
from app_db.schemas.order import *

scenarios("../features/orders.feature")

#Scenario 1
@given(parsers.parse('a user exists with ID {user_id:d}'))
def given_user_exists(db_session: Session, context: dict, user_id: int):
    user = get_user_by_id_db(db_session, UserById(id=user_id))
    if not user:
        user = create_user_db(
            db_session,
            UserCreate(
                name=f"user_{user_id}",
                email=f"user_{user_id}@gmail.com"
            )
        )
    context["user_id"] = user.id
@when(parsers.parse('I insert an order with user_id {user_id:d} item_name "{item_name}" and price {price:d}'))
def when_insert_order(db_session: Session, context: dict, user_id: int, item_name: str, price: int):
    actual_user_id = context.get("user_id", user_id)
    order = create_order_for_user_db(
        db_session,
        OrderCreate(
            user_id=actual_user_id,
            item_name=item_name,
            price=price
        )
    )
    context["order"] = order
    context["item_name"] = item_name
    context["price"] = price
@then('the order should exist in the database with correct details')
def then_validate_order(context: dict):
    order = context["order"]
    assert order is not None
    assert order.user_id == context["user_id"]
    assert order.item_name == context["item_name"]
    assert order.price == context["price"]


#Scenario 2
@given(parsers.parse('no user exists with ID {user_id:d}'))
def given_no_user_exists(db_session: Session, user_id: int):
    user = get_user_by_id_db(db_session, UserById(id=user_id))
    assert user is None
@when(parsers.parse('I try to insert an order with user_id {user_id:d}'))
def when_try_insert_order_invalid_user(db_session: Session, context: dict, user_id: int):
    try:
        create_order_for_user_db(
            db_session,
            OrderCreate(
                user_id=user_id,
                item_name="Mobile",
                price=100
            )
        )
    except IntegrityError as e:
        context["error"] = e
    else:
        context["error"] = None
@then('the database should raise a foreign key constraint error')
def then_verify_foreign_key_error(context: dict):
    error = context["error"]
    assert error is not None
    assert isinstance(error, IntegrityError)


#Scenario 3
@given('multiple orders exist')
def given_multiple_orders_exist(db_session: Session, context: dict):
    created_orders = []
    # Create 2 users + multiple orders
    for i in range(2):
        user = create_user_db(
            db_session,
            UserCreate(
                name=f"user_multi_{i}",
                email=f"user_multi_{i}@gmail.com"
            )
        )
        # Create 2 orders per user
        for j in range(2):
            order = create_order_for_user_db(
                db_session,
                OrderCreate(
                    user_id=user.id,
                    item_name=f"Item_{i}_{j}",
                    price=100 + j
                )
            )
            created_orders.append(order)
    context["expected_count"] = len(created_orders)
@when('I query all orders')
def when_query_all_orders(db_session: Session, context: dict):
    orders = get_orders_db(db_session)
    context["orders"] = orders
@then('all orders should be returned')
def then_validate_all_orders(context: dict):
    orders = context["orders"]
    assert orders is not None
    assert isinstance(orders, list)
    assert len(orders) >= context["expected_count"]
    for order in orders:
        assert isinstance(order.id, int)
        assert isinstance(order.user_id, int)
        assert isinstance(order.item_name, str)
        assert isinstance(order.price, int)


#Scenario 4
@given(parsers.parse('multiple orders exist for user ID {user_id:d}'))
def given_multiple_orders_for_user(db_session: Session, context: dict, user_id: int):
    # Ensure user exists
    user = get_user_by_id_db(db_session, UserById(id=user_id))
    if not user:
        user = create_user_db(
            db_session,
            UserCreate(
                name=f"user_{user_id}",
                email=f"user_{user_id}@gmail.com"
            )
        )

    actual_user_id = user.id
    context["user_id"] = actual_user_id

    created_orders = []

    # Create multiple orders for this user
    for i in range(3):
        order = create_order_for_user_db(
            db_session,
            OrderCreate(
                user_id=actual_user_id,
                item_name=f"Item_{i}",
                price=100 + i
            )
        )
        created_orders.append(order)

    context["expected_count"] = len(created_orders)
@when(parsers.parse('I query orders by user ID {user_id:d}'))
def when_query_orders_by_user(db_session: Session, context: dict, user_id: int):
    actual_user_id = context.get("user_id", user_id)
    orders = get_orders_by_user_id_db(
        db_session,
        UserById(id=actual_user_id)
    )
    context["orders"] = orders
@then(parsers.parse('all returned orders should belong to user ID {user_id:d}'))
def then_validate_orders_belong_to_user(context: dict, user_id: int):
    orders = context["orders"]
    actual_user_id = context.get("user_id", user_id)
    assert orders is not None
    assert len(orders) >= context["expected_count"]

    for order in orders:
        assert order.user_id == actual_user_id


#Scenario 5
@given(parsers.parse('an order exists with ID {order_id:d}'))
def given_order_exists_by_id(db_session: Session, context: dict, order_id: int):
    order = get_order_by_order_id_db(
        db_session,
        OrderById(id=order_id)
    )
    assert order is not None
    context["order_id"] = order.id
    context["expected_user_id"] = order.user_id
    context["expected_item_name"] = order.item_name
    context["expected_price"] = order.price
@when(parsers.parse('I query the order by ID {order_id:d}'))
def when_query_order_by_id(db_session: Session, context: dict, order_id: int):
    order = get_order_by_order_id_db(
        db_session,
        OrderById(id=order_id)
    )
    context["order"] = order
@then('the returned order should match stored values')
def then_validate_order_data(context: dict):
    order = context["order"]
    assert order is not None
    assert order.id == context["order_id"]
    assert order.user_id == context["expected_user_id"]
    assert order.item_name == context["expected_item_name"]
    assert order.price == context["expected_price"]


#Scenario 6
@when(parsers.parse('I update the order item_name to "{item_name}" and price to {price:d}'))
def when_update_order(db_session: Session, context: dict, item_name: str, price: int):
    updated_order = update_order_details_by_order_id_db(
        db_session,
        OrderById(id=context["order_id"]),
        OrderUpdate(
            user_id=context["expected_user_id"],
            item_name=item_name,
            price=price
        )
    )

    context["updated_order"] = updated_order
    context["new_item_name"] = item_name
    context["new_price"] = price
@then('the database should reflect updated order details')
def then_validate_updated_order(db_session: Session, context: dict):
    order = get_order_by_order_id_db(
        db_session,
        OrderById(id=context["order_id"])
    )
    assert order is not None
    assert order.item_name == context["new_item_name"]
    assert order.price == context["new_price"]
    # Ensure actual change happened
    assert order.item_name != context["expected_item_name"]
    assert order.price != context["expected_price"]


#Scenario 7
@when(parsers.parse('I delete orders using user ID {user_id:d}'))
def when_delete_orders_by_user(db_session: Session, context: dict, user_id: int):
    actual_user_id = context.get("user_id", user_id)
    delete_orders_by_user_id_db(
        db_session,
        UserById(id=actual_user_id)
    )
    context["deleted_user_id"] = actual_user_id
@then('no orders should exist for that user')
def then_verify_no_orders_for_user(db_session: Session, context: dict):
    orders = get_orders_by_user_id_db(
        db_session,
        UserById(id=context["deleted_user_id"])
    )
    assert orders is not None
    assert len(orders) == 0


#Scenario 8
@when(parsers.parse('I delete the order using order ID {order_id:d}'))
def when_delete_order_by_id(db_session: Session, context: dict, order_id: int):
    actual_order_id = context.get("order_id", order_id)
    delete_orders_by_order_id_db(
        db_session,
        OrderById(id=actual_order_id)
    )
    context["deleted_order_id"] = actual_order_id
@then('the order should not exist in the database')
def then_verify_order_deleted(db_session: Session, context: dict):
    order = get_order_by_order_id_db(
        db_session,
        OrderById(id=context["deleted_order_id"])
    )
    assert order is None