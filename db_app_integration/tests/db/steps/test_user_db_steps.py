from pytest_bdd import given, when, then, parsers, scenarios

from app_db.db.models.user import User
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

#Repository
from app_db.repository.user_repo import *

#Schemas
from app_db.schemas.user import *

scenarios("../features/users.feature")

@given(parsers.parse('I have a user payload with name "{name}" and email "{email}"'))
def given_user_payload(context:dict, name:str, email:str):
    payload = {"name":name,"email":email}
    context["payload"] = payload

@when(parsers.parse('I insert the user into the users table'))
def when_user_inserted_into_table(db_session:Session, context:dict):
    payload = context["payload"]
    user_data = UserCreate(name=payload["name"], email=payload["email"])
    user = create_user_db(db_session, user_data)
    context["user"] = user

@then(parsers.parse('the user should exist in the database with the correct name and email'))
def then_user_should_exist(context:dict):
    payload = context["payload"]
    user = context["user"]
    assert user.name == payload["name"]
    assert user.email == payload["email"]

@given(parsers.parse('a user already exists with name "{name}" and email "{email}"'))
def given_user_already_exist(db_session:Session, context:dict, name:str, email:str):
    user = UserCreate(name=name, email=email)
    created_user = create_user_db(db_session, user)
    context["existing_user"] = created_user

@when(parsers.parse('I try to insert another user with name "{name}" and email "{email}"'))
def when_insert_duplicate(db_session:Session, context:dict, name:str, email:str):
    user_data = UserCreate(name=name, email=email)
    try:
        create_user_db(db_session, user_data)
    except IntegrityError as e:
        context["error"] = e
    else:
        context["error"] = None

@then(parsers.parse('the database should raise a uniqueness constraint error'))
def then_raise_uniqueness_error(context:dict):
    error = context["error"]
    assert error is not None
    assert isinstance(error, IntegrityError)

@given(parsers.parse('a user exists with ID {user_id:d}'))
def given_user_exists(user_id:int):
    pass

@when(parsers.parse('I query the users table for user ID {user_id:d}'))
def when_query_user_by_id(db_session:Session, context:dict, user_id:int):
    user_data = get_user_by_id(db_session, UserById(id=user_id))
    context["user_data"] = user_data

@then(parsers.parse('the returned record should have user ID {user_id:d} the correct name and email'))
def then_validate_user_data(context:dict, user_id:int):
    user_data = context["user_data"]
    assert isinstance(user_data.name, str)
    assert isinstance(user_data.email, str)
    assert isinstance(user_data.id, int)
    assert user_data.id == user_id