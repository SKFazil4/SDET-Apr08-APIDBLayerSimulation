from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

#Repos
from app_db.repository.user_repo import *

#Depends
from app_db.api.deps import get_db

#Schema
from app_db.schemas.user import *

router = APIRouter(prefix="/users")



#Create
@router.post("/", response_model=UserResponse, tags=["Users - Insert"])
def create_user(user: UserCreate, db:Session=Depends(get_db)):
    user_exist = get_user_by_name_db(db, UserByName(name=user.name))
    if user_exist:
        raise HTTPException(status_code=409, detail=f"Username {user_exist.name} already exists")

    user_exist = get_user_by_mail_db(db, UserByEmail(email=user.email))
    if user_exist:
        raise HTTPException(status_code=409, detail=f"User mail {user_exist.email} already exists")

    user = create_user_db(db, user)
    if not user:
        raise HTTPException(status_code=500, detail="User not created")
    return user


#Read
@router.get("/", response_model=list[UserResponse], tags=["Users - Read"])
def get_user_details(db:Session=Depends(get_db)):
    user_exist = get_user_details_db(db)
    if not user_exist:
        raise HTTPException(status_code=404, detail=f"Users does not exists")
    return user_exist

@router.get("/id/{user_id}", response_model=UserResponse, tags=["Users - Read"])
def get_user_details_by_id(user_id:int, db:Session=Depends(get_db)):
    user_exist = get_user_by_id_db(db, UserById(id=user_id))
    if not user_exist:
        raise HTTPException(status_code=404, detail=f"User id {user_id} not exists")
    return user_exist

@router.get("/name/{user_name}", response_model=UserResponse, tags=["Users - Read"])
def get_user_details_by_user_name(user_name:str, db:Session=Depends(get_db)):
    user_exist = get_user_by_name_db(db, UserByName(name=user_name))
    if not user_exist:
        raise HTTPException(status_code=404, detail=f"Username {user_name} not exist")
    return user_exist

@router.get("/email/{user_email}", response_model=UserResponse, tags=["Users - Read"])
def get_user_details_by_user_email(user_email:str, db:Session=Depends(get_db)):
    user_exist = get_user_by_mail_db(db, UserByEmail(email=user_email))
    if not user_exist:
        raise HTTPException(status_code=404, detail=f"User mail {user_email} not exist")
    return user_exist


#Update
@router.put("/id/{user_id}", response_model=UserResponse, tags=["Users - Update"])
def update_user_details(user_id:int, user:UserUpdate, db:Session = Depends(get_db)):
    user_exist = get_user_by_id_db(db, UserById(id=user_id))
    if not user_exist:
        raise HTTPException(status_code=404, detail=f"User id {user_id} does not exist")
    user_name_exist = get_user_by_name_db(db, UserByName(name=user.name))
    if user_name_exist:
        if user_name_exist.name != user_exist.name:
            raise HTTPException(status_code=401, detail=f"Duplicate username {user.name}")
    user_email_exist = get_user_by_mail_db(db, UserByEmail(email=user.email))
    if user_email_exist:
        print("Email")
        if user_email_exist.email != user_exist.email:
            raise HTTPException(status_code=401, detail=f"Duplicate user email {user.email}")
    user = update_user_details_db(db, UserById(id=user_id), user)
    if not user:
        raise HTTPException(status_code=500, detail="User not updated")
    return user


#Delete
@router.delete("/id/{user_id}", tags=["Users - Delete"])
def delete_user_by_id(user_id:int, db:Session = Depends(get_db)):
    user_exist = get_user_by_id_db(db, UserById(id=user_id))
    if not user_exist:
        raise HTTPException(status_code=404, detail=f"User id {user_id} does not exist")
    delete_user_by_id_db(db, UserById(id=user_id))
    return {"response": f"User {user_id} has been deleted successfully"}

@router.delete("/name/{user_name}", tags=["Users - Delete"])
def delete_user_by_name(user_name:str, db:Session = Depends(get_db)):
    user_exist = get_user_by_name_db(db, UserByName(name=user_name))
    if not user_exist:
        raise HTTPException(status_code=404, detail=f"Username {user_name} does not exist")
    delete_user_by_name_db(db, UserByName(name=user_name))
    return {"response":f"User {user_name} has been deleted successfully"}