from pytest_bdd import given, when, then, parsers, scenarios

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

#Repository
from app_db.repository.user_repo import get_user_by_id
from app_db.repository.profile_repo import *

#Schemas
from app_db.schemas.user import UserWithRelations


scenarios("../features/profiles.feature")

@given(parsers.parse('a user exists with ID {user_id:d}'))
def given_user_exists(user_id:int):
    pass

@given(parsers.parse('I have a profile payload with user_id {user_id:d} and bio "{bio_data}"'))
def given_profile_payload(context:dict, user_id:int, bio_data:str):
    context["payload"] = {"user_id":user_id, "bio_data":bio_data}

@when("I insert the profile into the profiles table")
def when_insert_profile_data(db_session:Session, context:dict):
    payload = context["payload"]
    profile_data = create_profile_db(db_session, UserWithRelations(user_id=payload["user_id"], bio=payload["bio_data"]))
    context["profile_data"] = profile_data

@then("the profile should exist with the correct user_id and bio")
def then_user_data_should_exist(context:dict):
    payload = context["payload"]
    profile_data = context["profile_data"]
    assert payload["user_id"] == profile_data.user_id
    assert payload["bio_data"] == profile_data.bio

#Scenario 2
@given(parsers.parse('no user exists with ID {user_id:d}'))
def given_user_does_not_exists(db_session:Session, user_id:int):
    user = get_user_by_id(db_session, UserById(id=user_id))
    assert user is None

@when(parsers.parse('I try to insert a profile with user_id {user_id:d}'))
def when_try_to_insert_profile(db_session:Session, context:dict, user_id:int):
    try:
        create_profile_db(db_session, UserWithRelations(user_id=user_id, bio="Hi I'm new here"))
    except IntegrityError as e:
        context["error"] = e
    else:
        context["error"] = None

@then("the database should raise a foreign key constraint error")
def then_check_for_foreign_key_error(context:dict):
    error = context["error"]
    assert error is not None
    assert isinstance(error,IntegrityError)

#Scenario 3
@given(parsers.parse('a profile already exists for user ID {user_id:d}'))
def given_user_profile_exists(db_session:Session, user_id:int):
    profile = get_profile_by_user_id_db(db_session, UserById(id=user_id))
    assert profile.user_id == user_id
    assert profile.bio is not None

@when(parsers.parse('I try to insert another profile for user ID {user_id:d}'))
def when_try_to_insert_profile(db_session:Session, context:dict, user_id:int):
    try:
        create_profile_db(db_session, UserWithRelations(user_id=user_id, bio="Hi I'm new here"))
    except IntegrityError as e:
        context["error"] = e
    else:
        context["error"] = None
@then("the database should raise a uniqueness constraint error")
def then_check_for_uniqueness_error(context:dict):
    error = context["error"]
    assert error is not None
    assert isinstance(error,IntegrityError)

#Scenario 4

@when(parsers.parse('I query the profiles table by user ID {user_id:d}'))
def when_query_profile(db_session:Session, context:dict, user_id:int):
    profile = get_profile_by_user_id_db(db_session, UserById(id=user_id))
    context["profile"] = profile

@then("the returned profile should have the correct bio")
def then_check_profile_data(context:dict):
     profile = context["profile"]
     assert isinstance(profile.user_id,int)
     assert isinstance(profile.bio,str)
     assert profile.bio is not None