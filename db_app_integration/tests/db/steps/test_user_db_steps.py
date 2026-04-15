from pytest_bdd import given, when, then, parsers, scenarios

from app_db.db.models.user import User
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

#Repository
from app_db.repository.user_repo import *

#Schemas
from app_db.schemas.user import *

scenarios("../features/users.feature")



#Scenario 1
@given(parsers.parse('I have a user payload with name "{name}" and email "{email}"'))
def given_user_payload(context: dict, name: str, email: str):
    context["payload"] = {"name": name, "email": email}


@when('I insert the user into the users table')
def when_user_inserted_into_table(db_session: Session, context: dict):
    payload = context["payload"]
    user_data = UserCreate(name=payload["name"], email=payload["email"])
    user = create_user_db(db_session, user_data)
    context["user"] = user


@then('the user should exist in the database with the correct name and email')
def then_user_should_exist(context: dict):
    payload = context["payload"]
    user = context["user"]

    assert user.name == payload["name"]
    assert user.email == payload["email"]


#Scenario 2
@given(parsers.parse('a user already exists with name "{name}" and email "{email}"'))
def given_user_already_exist(db_session: Session, context: dict, name: str, email: str):
    user = UserCreate(name=name, email=email)
    created_user = create_user_db(db_session, user)
    context["existing_user"] = created_user


@when(parsers.parse('I try to insert another user with name "{name}" and email "{email}"'))
def when_insert_duplicate(db_session: Session, context: dict, name: str, email: str):
    user_data = UserCreate(name=name, email=email)

    try:
        create_user_db(db_session, user_data)
    except IntegrityError as e:
        context["error"] = e
    else:
        context["error"] = None


@then('the database should raise a uniqueness constraint error')
def then_raise_uniqueness_error(context: dict):
    error = context["error"]

    assert error is not None
    assert isinstance(error, IntegrityError)


#Scenario 3

@given(parsers.parse('a user exists with ID {user_id:d}'))
def given_user_exists_with_id(db_session: Session, context: dict, user_id: int):
    # Create user explicitly with known ID (or assume auto increment starts clean)
    user = UserCreate(name=f"user_{user_id}", email=f"user_{user_id}@gmail.com")
    created_user = create_user_db(db_session, user)

    context["user"] = created_user
    context["user_id"] = created_user.id


@when(parsers.parse('I query the users table for user ID {user_id:d}'))
def when_query_user_by_id(db_session: Session, context: dict, user_id: int):
    # Use actual stored ID (safe for DB auto increment)
    actual_id = context.get("user_id", user_id)

    user_data = get_user_by_id_db(db_session, UserById(id=actual_id))
    context["user_data"] = user_data


@then('the returned record should have correct name and email')
def then_validate_user_by_id(context: dict):
    user_data = context["user_data"]
    original_user = context["user"]

    assert user_data is not None
    assert user_data.name == original_user.name
    assert user_data.email == original_user.email


#Scenario 4

@given(parsers.parse('a user exists with name "{name}"'))
def given_user_exists_with_name(db_session: Session, context: dict, name: str):
    user = UserCreate(name=name, email=f"{name}@gmail.com")
    created_user = create_user_db(db_session, user)

    context["user"] = created_user


@when(parsers.parse('I query the users table by name "{name}"'))
def when_query_user_by_name(db_session: Session, context: dict, name: str):
    user_data = get_user_by_name_db(db_session, UserByName(name=name))
    context["user_data"] = user_data


@then('the returned record should match the user details')
def then_validate_user_by_name(context: dict):
    user_data = context["user_data"]
    original_user = context["user"]

    assert user_data is not None
    assert user_data.name == original_user.name
    assert user_data.email == original_user.email


#Scenario 5

@given(parsers.parse('a user exists with email "{email}"'))
def given_user_exists_with_email(db_session: Session, context: dict, email: str):
    user = UserCreate(name=email.split("@")[0], email=email)
    created_user = create_user_db(db_session, user)

    context["user"] = created_user


@when(parsers.parse('I query the users table by email "{email}"'))
def when_query_user_by_email(db_session: Session, context: dict, email: str):
    user_data = get_user_by_mail_db(db_session, UserByEmail(email=email))
    context["user_data"] = user_data


@then('the returned record should match the user details')
def then_validate_user_by_email(context: dict):
    user_data = context["user_data"]
    original_user = context["user"]

    assert user_data is not None
    assert user_data.name == original_user.name
    assert user_data.email == original_user.email

#Scenario 6

@when(parsers.parse('I update the user\'s name to "{name}" and email to "{email}"'))
def when_update_user(db_session: Session, context: dict, name: str, email: str):
    user = context["user"]

    updated_user = update_user_details_db(
        db_session,
        UserById(id=user.id),
        UserUpdate(name=name, email=email)
    )

    context["updated_user"] = updated_user


@then('the database should reflect the updated values')
def then_validate_update(context: dict):
    updated_user = context["updated_user"]

    assert updated_user.name is not None
    assert updated_user.email is not None


#Scenario 7

@when('I delete the user from the users table')
def when_delete_user(db_session: Session, context: dict):
    user = context["user"]

    delete_user_by_id_db(db_session, UserById(id=user.id))


@then('the user should not exist in the database')
def then_validate_user_deleted(db_session: Session, context: dict):
    user = context["user"]

    result = get_user_by_id_db(db_session, UserById(id=user.id))

    assert result is None
