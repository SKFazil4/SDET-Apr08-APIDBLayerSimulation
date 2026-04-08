from sqlalchemy import select, insert, update, delete, or_
from app_db.schemas.user import *
from app_db.db.models.profile import Profile
from sqlalchemy.orm import Session


def create_profile_db(session:Session, profile:UserWithRelations):
    stmt = (
        insert(Profile)
        .values(user_id=profile.user_id, bio=profile.bio)
        .returning(Profile)
    )
    result = session.execute(stmt)
    session.commit()
    return result.scalar_one()

def get_profile_by_user_id_db(session:Session, user_id:UserById):
    stmt = select(Profile).where(Profile.user_id == user_id.id)
    result = session.execute(stmt).scalar_one_or_none()
    return result