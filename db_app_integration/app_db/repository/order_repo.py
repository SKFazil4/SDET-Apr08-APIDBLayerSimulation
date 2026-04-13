from sqlalchemy import select, insert, update, delete, or_
from app_db.schemas.order import *
from app_db.schemas.user import UserById
from app_db.db.models.order import Order
from sqlalchemy.orm import Session

#Create
def create_order_for_user_db(session:Session, order:OrderCreate):
    stmt = (
        insert(Order)
        .values(user_id=order.user_id, item_name=order.item_name, price=order.price)
        .returning(Order)
    )
    result = session.execute(stmt)
    session.commit()
    return result.scalar_one()


#Read
def get_orders_db(session:Session):
    stmt = select(Order)
    result = session.execute(stmt).scalars().all()
    return result

def get_orders_by_user_id_db(session:Session, user_id:UserById):
    stmt = (
        select(Order)
        .where(Order.user_id == user_id.id)
    )
    result = session.execute(stmt).scalars().all()
    return result

def get_order_by_order_id_db(session:Session, order_id:OrderById):
    stmt = select(Order).where(Order.id == order_id.id)
    result = session.execute(stmt).scalar_one_or_none()
    return result


#Update
def update_order_details_by_order_id_db(session:Session, order_id:OrderById, order:OrderUpdate):
    data={
        "user_id":order.user_id,
        "item_name":order.item_name,
        "price":order.price
    }
    stmt = update(Order).where(Order.id == order_id.id).values(**data).returning(Order)
    result = session.execute(stmt)
    session.commit()
    return result.scalar_one()


#Delete
def delete_orders_by_user_id_db(session:Session, user_id:UserById):
    stmt = delete(Order).where(Order.user_id == user_id.id)
    session.execute(stmt)
    session.commit()

def delete_orders_by_order_id_db(session:Session, order_id:OrderById):
    stmt = delete(Order).where(Order.id == order_id.id)
    session.execute(stmt)
    session.commit()