from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

#Repos
from app_db.repository.order_repo import *
from app_db.repository.user_repo import *

#Depends
from app_db.api.deps import get_db

#Schema
from app_db.schemas.order import *

router = APIRouter(prefix="/orders")


#Create
@router.post("/", response_model=OrderResponse, tags=["Orders - Insert"])
def create_order_for_user(order:OrderCreate ,db:Session=Depends(get_db)):
    user_exist = get_user_by_id_db(db, UserById(id=order.user_id))
    if not user_exist:
        raise HTTPException(status_code=404, detail="User does not exists")

    order = create_order_for_user_db(db, order)
    if not order:
        raise HTTPException(status_code=500, detail="Order not created")

    return order


#Read
@router.get("/", response_model=list[OrderResponse], tags=["Orders - Read"])
def get_order_details(db:Session = Depends(get_db)):
    orders = get_orders_db(db)
    if not orders:
        raise HTTPException(status_code=404, detail="orders does not exist")
    return orders

@router.get("/userid/{user_id}", response_model=list[OrderResponse], tags=["Orders - Read"])
def get_order_details_by_user_id(user_id:int, db:Session = Depends(get_db)):
    user_exist = get_user_by_id_db(db, UserById(id=user_id))
    if not user_exist:
        raise HTTPException(status_code=404, detail="User not exists")
    orders = get_orders_by_user_id_db(db, UserById(id=user_id))
    if not orders:
        raise HTTPException(status_code=404, detail="orders does not exist")
    return orders

@router.get("/orderid/{order_id}", response_model=OrderResponse, tags=["Orders - Read"])
def get_order_details_by_order_id(order_id:int, db:Session = Depends(get_db)):
    order_exist = get_order_by_order_id_db(db, OrderById(id=order_id))
    if not order_exist:
        raise HTTPException(status_code=404, detail="order does not exist")
    return order_exist


#Update
@router.put("/id/{order_id}", tags=["Orders - Update"])
def update_order_details_by_order_id(order_id:int, order:OrderUpdate, db:Session = Depends(get_db)):
    order_exist = get_order_by_order_id_db(db, OrderById(id=order_id))
    if not order_exist:
        raise HTTPException(status_code=404, detail="Order does not exists")
    order_detail = update_order_details_by_order_id_db(db, OrderById(id=order_id), order)
    if not order_detail:
        raise HTTPException(status_code=404, detail="Order not updated")
    return order_detail


#Delete
@router.delete("/userid/{user_id}", tags=["Orders - Delete"])
def delete_order_details_by_user_id(user_id:int, db:Session = Depends(get_db)):
    user_exist = get_user_by_id_db(db, UserById(id=user_id))
    if not user_exist:
        raise HTTPException(status_code=404, detail="User not exists")
    delete_orders_by_user_id_db(db, UserById(id=user_id))
    return {"response": f"Order with user Id {user_id} has been deleted successfully"}

@router.delete("/orderid/{order_id}", tags=["Orders - Delete"])
def delete_order_details_by_user_id(order_id:int, db:Session = Depends(get_db)):
    order = get_order_by_order_id_db(db, OrderById(id=order_id))
    if not order:
        raise HTTPException(status_code=404, detail="Order does not exists")
    delete_orders_by_order_id_db(db, OrderById(id=order_id))
    return {"response": f"Order with user Id {order_id} has been deleted successfully"}