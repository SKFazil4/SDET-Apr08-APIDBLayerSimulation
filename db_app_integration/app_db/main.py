from fastapi import FastAPI, HTTPException, Depends

#Local Session
from app_db.db.session import SessionLocal, engine

#Base
from app_db.db.base import Base

#Schema
from app_db.schemas.order import *
from app_db.schemas.user import *
from app_db.schemas.profile import *

#Repo
from app_db.repository.user_repo import *
from app_db.repository.profile_repo import *
from app_db.repository.order_repo import *

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#User
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db:Session=Depends(get_db)):
    user_exist = get_user_by_name(db, UserByName(name=user.name))
    if user_exist:
        raise HTTPException(status_code=409, detail="User name already exists")

    user_exist = get_user_by_mail(db, UserByEmail(email=user.email))
    if user_exist:
        raise HTTPException(status_code=409, detail="User mail already exists")

    user = create_user_db(db, user)
    if not user:
        raise HTTPException(status_code=500, detail="User not created")
    return user

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user_details(user_id:int, db:Session=Depends(get_db)):
    user_exist = get_user_by_id(db, UserById(id=user_id))
    if not user_exist:
        raise HTTPException(status_code=404, detail="User not exists")
    return user_exist


#Profile
@app.post("/profiles", response_model=ProfileResponse)
def create_user_profile(profile:UserWithRelations, db:Session=Depends(get_db)):
    user_profile_exist = get_profile_by_user_id_db(db, UserById(id=profile.user_id))
    if user_profile_exist:
        raise HTTPException(status_code=409, detail="User profile already exists")

    user_exist = get_user_by_id(db, UserById(id=profile.user_id))
    if not user_exist:
        raise HTTPException(status_code=409, detail="User does not exists")

    profile = create_profile_db(db, profile)
    if not profile:
        raise HTTPException(status_code=500, detail="Profile not created")

    return profile


#Order
@app.post("/orders", response_model=OrderResponse)
def create_order_for_user(order:OrderCreate ,db:Session=Depends(get_db)):
    user_exist = get_user_by_id(db, UserById(id=order.user_id))
    if not user_exist:
        raise HTTPException(status_code=404, detail="User profile does not exists")

    order = create_order_for_user_db(db, order)
    if not order:
        raise HTTPException(status_code=500, detail="Order not created")

    return order

# Base.metadata.create_all(bind=engine)