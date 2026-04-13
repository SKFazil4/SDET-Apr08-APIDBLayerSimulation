from sqlalchemy import select, insert, update, delete, or_
from sqlalchemy.orm import Session
#schema
from app_db.schemas.user import *
from app_db.schemas.profile import *
#Model
from app_db.db.models.profile import Profile

#Create
def create_profile_db(session:Session, profile:ProfileCreate):
    stmt = (
        insert(Profile)
        .values(user_id=profile.user_id, bio=profile.bio)
        .returning(Profile)
    )
    result = session.execute(stmt)
    session.commit()
    return result.scalar_one()


#Read
def get_profile_details_db(session:Session):
    stmt = select(Profile)
    result = session.execute(stmt).scalars().all()
    return result

def get_profile_by_user_id_db(session:Session, user_id:UserById):
    stmt = select(Profile).where(Profile.user_id == user_id.id)
    result = session.execute(stmt).scalar_one_or_none()
    return result

def get_profile_by_profile_id_db(session:Session, profile_id:ProfileById):
    stmt = select(Profile).where(Profile.id == profile_id.id)
    result = session.execute(stmt).scalar_one_or_none()
    return result


#Update
def update_profile_details_by_user_id_db(session:Session, user_id:UserById, profile:ProfileUpdate):
    stmt = update(Profile).where(Profile.user_id==user_id.id).values(bio = profile.bio).returning(Profile)
    result = session.execute(stmt)
    session.commit()
    return result.scalar_one()


#Delete
def delete_profile_details_by_user_id_db(session:Session, user_id:UserById):
    stmt = delete(Profile).where(Profile.user_id == user_id.id)
    session.execute(stmt)
    session.commit()

def delete_profile_details_by_profile_id_db(session:Session, profile_id:ProfileById):
    stmt = delete(Profile).where(Profile.id == profile_id.id)
    session.execute(stmt)
    session.commit()