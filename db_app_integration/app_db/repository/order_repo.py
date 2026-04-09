from sqlalchemy import select, insert, update, delete, or_
from app_db.schemas.order import *
from app_db.schemas.user import UserById
from app_db.db.models.order import Order
from sqlalchemy.orm import Session

def create_order_for_user_db(session:Session, order:OrderCreate):
    stmt = (
        insert(Order)
        .values(user_id=order.user_id, item_name=order.item_name, price=order.price)
        .returning(Order)
    )
    result = session.execute(stmt)
    session.commit()
    return result.scalar_one()

def get_orders_by_user_id(session:Session, user_id:UserById):
    stmt = (
        select(Order)
        .where(Order.user_id == user_id.id)
    )
    result = session.execute(stmt).scalars().all()
    return result