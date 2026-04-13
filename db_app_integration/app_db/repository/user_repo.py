from sqlalchemy import select, insert, update, delete, or_
from app_db.schemas.user import *
from app_db.db.models.user import User
from sqlalchemy.orm import Session, joinedload

#Create
def create_user_db(session:Session, user:UserCreate):
    stmt =  insert(User).values(name = user.name, email = user.email).returning(User)
    result = session.execute(stmt)
    session.commit()
    return result.scalar_one()


#Read
def get_user_details_db(session:Session):
    stmt = select(User)
    result = session.execute(stmt).scalars().all()
    return result

def get_user_db(session:Session, user:UserCreate):
    stmt = select(User).where(or_(User.name == user.name, User.email == user.email))
    result = session.execute(stmt).scalar_one_or_none()
    return result

def get_user_by_name_db(session:Session, user:UserByName):
    stmt = select(User).where(User.name == user.name)
    result = session.execute(stmt).scalar_one_or_none()
    return result

def get_user_by_mail_db(session:Session, user:UserByEmail):
    stmt = select(User).where(User.email == user.email)
    result = session.execute(stmt).scalar_one_or_none()
    return result

def get_user_by_id_db(session:Session, user:UserById):
    stmt = select(User).where(User.id == user.id)
    result = session.execute(stmt).scalar_one_or_none()
    return result


#Update
def update_user_details_db(session:Session, user_id:UserById, user:UserUpdate):
    data = {
        "name":user.name,
        "email":user.email
    }
    stmt = update(User).where(User.id == user_id.id).values(**data).returning(User)
    result = session.execute(stmt)
    session.commit()
    return result.scalar_one()


#Delete
def delete_user_by_id_db(session:Session, user_id:UserById):
    stmt = delete(User).where(User.id == user_id.id)
    session.execute(stmt)
    session.commit()

def delete_user_by_name_db(session:Session, user_name:UserByName):
    stmt = delete(User).where(User.name == user_name.name)
    session.execute(stmt)
    session.commit()