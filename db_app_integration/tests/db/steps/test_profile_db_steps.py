from pytest_bdd import given, when, then, parsers, scenarios

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

#Repository
from app_db.repository.user_repo import *
from app_db.repository.profile_repo import *

#Schemas
from app_db.schemas.profile import ProfileCreate


scenarios("../features/profiles.feature")

# @given(parsers.parse('a user exists with ID {user_id:d}'))
# def given_user_exists(user_id:int):
#     pass
#
# @given(parsers.parse('I have a profile payload with user_id {user_id:d} and bio "{bio_data}"'))
# def given_profile_payload(context:dict, user_id:int, bio_data:str):
#     context["payload"] = {"user_id":user_id, "bio_data":bio_data}
#
# @when("I insert the profile into the profiles table")
# def when_insert_profile_data(db_session:Session, context:dict):
#     payload = context["payload"]
#     profile_data = create_profile_db(db_session, ProfileCreate(user_id=payload["user_id"], bio=payload["bio_data"]))
#     context["profile_data"] = profile_data
#
# @then("the profile should exist with the correct user_id and bio")
# def then_user_data_should_exist(context:dict):
#     payload = context["payload"]
#     profile_data = context["profile_data"]
#     assert payload["user_id"] == profile_data.user_id
#     assert payload["bio_data"] == profile_data.bio
#
# #Scenario 2
# @given(parsers.parse('no user exists with ID {user_id:d}'))
# def given_user_does_not_exists(db_session:Session, user_id:int):
#     user = get_user_by_id_db(db_session, UserById(id=user_id))
#     assert user is None
#
# @when(parsers.parse('I try to insert a profile with user_id {user_id:d}'))
# def when_try_to_insert_profile(db_session:Session, context:dict, user_id:int):
#     try:
#         create_profile_db(db_session, ProfileCreate(user_id=user_id, bio="Hi I'm new here"))
#     except IntegrityError as e:
#         context["error"] = e
#     else:
#         context["error"] = None
#
# @then("the database should raise a foreign key constraint error")
# def then_check_for_foreign_key_error(context:dict):
#     error = context["error"]
#     assert error is not None
#     assert isinstance(error,IntegrityError)
#
# #Scenario 3
# @given(parsers.parse('a profile already exists for user ID {user_id:d}'))
# def given_user_profile_exists(db_session:Session, user_id:int):
#     profile = get_profile_by_user_id_db(db_session, UserById(id=user_id))
#     assert profile.user_id == user_id
#     assert profile.bio is not None
#
# @when(parsers.parse('I try to insert another profile for user ID {user_id:d}'))
# def when_try_to_insert_profile(db_session:Session, context:dict, user_id:int):
#     try:
#         create_profile_db(db_session, ProfileCreate(user_id=user_id, bio="Hi I'm new here"))
#     except IntegrityError as e:
#         context["error"] = e
#     else:
#         context["error"] = None
# @then("the database should raise a uniqueness constraint error")
# def then_check_for_uniqueness_error(context:dict):
#     error = context["error"]
#     assert error is not None
#     assert isinstance(error,IntegrityError)
#
# #Scenario 4
#
# @when(parsers.parse('I query the profiles table by user ID {user_id:d}'))
# def when_query_profile(db_session:Session, context:dict, user_id:int):
#     profile = get_profile_by_user_id_db(db_session, UserById(id=user_id))
#     context["profile"] = profile
#
# @then("the returned profile should have the correct bio")
# def then_check_profile_data(context:dict):
#      profile = context["profile"]
#      assert isinstance(profile.user_id,int)
#      assert isinstance(profile.bio,str)
#      assert profile.bio is not None


#Scenario 1
@given(parsers.parse('a user exists with ID {user_id:d}'))
def given_user_exists(db_session: Session, context: dict, user_id: int):
    user = get_user_by_id_db(db_session, UserById(id=user_id))
    if not user:
        created_user = create_user_db(
            db_session,
            UserCreate(
                name=f"user_{user_id}",
                email=f"user_{user_id}@test.com"
            )
        )
        context["user_id"] = created_user.id
    else:
        context["user_id"] = user.id
@when(parsers.parse('I insert a profile with user_id {user_id:d} and bio "{bio}"'))
def when_insert_profile(db_session: Session, context: dict, user_id: int, bio: str):
    actual_user_id = context.get("user_id", user_id)
    profile = create_profile_db(
        db_session,
        ProfileCreate(user_id=actual_user_id, bio=bio)
    )

    context["profile"] = profile
    context["bio"] = bio
@then('the profile should exist in the database with correct user_id and bio')
def then_profile_created(context: dict):
    profile = context["profile"]
    assert profile is not None
    assert profile.user_id == context["user_id"]
    assert profile.bio == context["bio"]


#Scenario 2
@given(parsers.parse('a profile already exists for user ID {user_id:d}'))
def given_profile_exists(db_session: Session, context: dict, user_id: int):
    user = get_user_by_id_db(db_session, UserById(id=user_id))
    if not user:
        user = create_user_db(
            db_session,
            UserCreate(
                name=f"user_{user_id}",
                email=f"user_{user_id}@test.com"
            )
        )
    actual_user_id = user.id
    context["user_id"] = actual_user_id

    profile = get_profile_by_user_id_db(
        db_session, UserById(id=actual_user_id)
    )
    if not profile:
        profile = create_profile_db(
            db_session,
            ProfileCreate(
                user_id=actual_user_id,
                bio="Existing Bio"
            )
        )

    context["existing_profile"] = profile
@when(parsers.parse('I try to insert another profile for user ID {user_id:d}'))
def when_insert_duplicate_profile(db_session: Session, context: dict, user_id: int):
    actual_user_id = context.get("user_id", user_id)
    try:
        create_profile_db(
            db_session,
            ProfileCreate(
                user_id=actual_user_id,
                bio="Duplicate Bio"
            )
        )
    except IntegrityError as e:
        context["error"] = e
    else:
        context["error"] = None
@then('the database should raise a uniqueness constraint error')
def then_uniqueness_error(context: dict):
    error = context["error"]
    assert error is not None
    assert isinstance(error, IntegrityError)


#Scenario 3
@given(parsers.parse('no user exists with ID {user_id:d}'))
def given_no_user_exists(db_session: Session, user_id: int):
    user = get_user_by_id_db(db_session, UserById(id=user_id))
    assert user is None
@when(parsers.parse('I try to insert a profile with user_id {user_id:d}'))
def when_insert_profile_invalid_user(db_session: Session, context: dict, user_id: int):
    try:
        create_profile_db(
            db_session,
            ProfileCreate(
                user_id=user_id,
                bio="Invalid user profile"
            )
        )
    except IntegrityError as e:
        context["error"] = e
    else:
        context["error"] = None
@then('the database should raise a foreign key constraint error')
def then_fk_constraint_error(context: dict):
    error = context["error"]
    assert error is not None
    assert isinstance(error, IntegrityError)


#Scenario 4
@given(parsers.parse('a profile exists for user ID {user_id:d}'))
def given_profile_exists(db_session: Session, context: dict, user_id: int):
    user = get_user_by_id_db(db_session, UserById(id=user_id))
    if not user:
        user = create_user_db(
            db_session,
            UserCreate(
                name=f"user_{user_id}",
                email=f"user_{user_id}@test.com"
            )
        )

    profile = get_profile_by_user_id_db(
        db_session,
        UserById(id=user.id)
    )

    if not profile:
        profile = create_profile_db(
            db_session,
            ProfileCreate(
                user_id=user.id,
                bio="Test Bio"
            )
        )

    context["user_id"] = user.id
    context["expected_bio"] = profile.bio
@when(parsers.parse('I query the profile by user ID {user_id:d}'))
def when_query_profile_by_user_id(db_session: Session, context: dict, user_id: int):
    actual_user_id = context.get("user_id", user_id)
    profile = get_profile_by_user_id_db(
        db_session,
        UserById(id=actual_user_id)
    )
    context["profile"] = profile
@then('the returned profile should have correct bio')
def then_validate_profile_bio(context: dict):
    profile = context["profile"]
    assert profile is not None
    assert profile.user_id == context["user_id"]
    assert profile.bio == context["expected_bio"]


#Scenario 5
@given(parsers.parse('a profile exists with profile ID {profile_id:d}'))
def given_profile_exists_by_id(db_session: Session, context: dict, profile_id: int):
    profile = get_profile_by_profile_id_db(
        db_session,
        ProfileById(id=profile_id)
    )
    assert profile is not None
    context["profile_id"] = profile.id
    context["expected_user_id"] = profile.user_id
    context["expected_bio"] = profile.bio
@when(parsers.parse('I query the profile by profile ID {profile_id:d}'))
def when_query_profile_by_id(db_session: Session, context: dict, profile_id: int):
    profile = get_profile_by_profile_id_db(
        db_session,
        ProfileById(id=profile_id)
    )
    context["profile"] = profile
@then('the returned profile should match the stored data')
def then_validate_full_profile(context: dict):
    profile = context["profile"]
    assert profile is not None
    assert profile.id == context["profile_id"]
    assert profile.user_id == context["expected_user_id"]
    assert profile.bio == context["expected_bio"]


#Scenario 6
@when(parsers.parse('I update the profile bio to "{bio}"'))
def when_update_profile_bio(db_session: Session, context: dict, bio: str):

    updated_profile = update_profile_details_by_user_id_db(
        db_session,
        UserById(id=context["user_id"]),
        ProfileUpdate(bio=bio)
    )

    context["updated_profile"] = updated_profile
    context["new_bio"] = bio
@then('the database should reflect the updated bio')
def then_validate_updated_bio(db_session: Session, context: dict):

    profile = get_profile_by_user_id_db(
        db_session,
        UserById(id=context["user_id"])
    )

    assert profile is not None
    assert profile.bio == context["new_bio"]
    assert profile.bio != context["expected_bio"]


#Scenario 7
@when(parsers.parse('I delete the profile using user ID {user_id:d}'))
def when_delete_profile_by_user_id(db_session: Session, context: dict, user_id: int):
    actual_user_id = context.get("user_id", user_id)

    delete_profile_details_by_user_id_db(
        db_session,
        UserById(id=actual_user_id)
    )

    context["deleted_user_id"] = actual_user_id
@then('the profile should not exist in the database')
def then_verify_profile_deleted(db_session: Session, context: dict):
    profile = None
    if "deleted_user_id" in context:
        profile = get_profile_by_user_id_db(
            db_session,
            UserById(id=context["deleted_user_id"])
        )
    elif "deleted_profile_id" in context:
        profile = get_profile_by_profile_id_db(
            db_session,
            ProfileById(id=context["deleted_profile_id"])
        )

    assert profile is None


#Scenario 8
@when(parsers.parse('I delete the profile using profile ID {profile_id:d}'))
def when_delete_profile_by_id(db_session: Session, context: dict, profile_id: int):

    actual_profile_id = context.get("profile_id", profile_id)

    delete_profile_details_by_profile_id_db(
        db_session,
        ProfileById(id=actual_profile_id)
    )

    context["deleted_profile_id"] = actual_profile_id