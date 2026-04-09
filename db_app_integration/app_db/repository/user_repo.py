from sqlalchemy import select, insert, update, delete, or_
from app_db.schemas.user import *
from app_db.db.models.user import User
from sqlalchemy.orm import Session, joinedload


def create_user_db(session:Session, user:UserCreate):
    stmt =  insert(User).values(name = user.name, email = user.email).returning(User)
    result = session.execute(stmt)
    session.commit()
    return result.scalar_one()

def get_user_db(session:Session, user:UserCreate):
    stmt = select(User).where(or_(User.name == user.name, User.email == user.email))
    result = session.execute(stmt).scalar_one_or_none()
    return result

def get_user_by_name(session:Session, user:UserByName):
    stmt = select(User).where(User.name == user.name)
    result = session.execute(stmt).scalar_one_or_none()
    return result

def get_user_by_mail(session:Session, user:UserByEmail):
    stmt = select(User).where(User.email == user.email)
    result = session.execute(stmt).scalar_one_or_none()
    return result

def get_user_by_id(session:Session, user:UserById):
    stmt = select(User).where(User.id == user.id)
    result = session.execute(stmt).scalar_one_or_none()
    return result
