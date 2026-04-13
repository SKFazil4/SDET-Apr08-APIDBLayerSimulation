from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

#Repos
from app_db.repository.user_repo import *
from app_db.repository.profile_repo import *

#Depends
from app_db.api.deps import get_db

#Schema
from app_db.schemas.profile import *

router = APIRouter(prefix="/profiles")

#Create
@router.post("/", response_model=ProfileResponse, tags=["Profiles - Insert"])
def create_user_profile(profile:ProfileCreate, db:Session=Depends(get_db)):
    user_profile_exist = get_profile_by_user_id_db(db, UserById(id=profile.user_id))
    if user_profile_exist:
        raise HTTPException(status_code=409, detail="User profile already exists")

    user_exist = get_user_by_id_db(db, UserById(id=profile.user_id))
    if not user_exist:
        raise HTTPException(status_code=409, detail=f"User id {profile.user_id} does not exists")

    profile = create_profile_db(db, profile)
    if not profile:
        raise HTTPException(status_code=500, detail="Profile not created")

    return profile


#Read
@router.get("/", response_model=list[ProfileResponse], tags=["Profiles - Read"])
def get_profile_details(db:Session = Depends(get_db)):
    profiles = get_profile_details_db(db)
    if not profiles:
        raise HTTPException(status_code=404, detail=f"Profiles does not exists")
    return profiles

@router.get("/userid/{user_id}", response_model=ProfileResponse, tags=["Profiles - Read"])
def get_profile_details_by_user_id(user_id:int, db:Session = Depends(get_db)):
    user_exist = get_user_by_id_db(db, UserById(id=user_id))
    if not user_exist:
        raise HTTPException(status_code=404, detail="User not exists")
    profile = get_profile_by_user_id_db(db, UserById(id=user_id))
    if not profile:
        raise HTTPException(status_code=404, detail="profile does not exist")
    return profile

@router.get("/profileid/{profile_id}", response_model=ProfileResponse, tags=["Profiles - Read"])
def get_profile_details_by_profile_id(profile_id:int, db:Session = Depends(get_db)):
    profile_exist = get_profile_by_profile_id_db(db, ProfileById(id=profile_id))
    if not profile_exist:
        raise HTTPException(status_code=404, detail="Profile not exist")
    return profile_exist


#Update
@router.put("/id/{user_id}", response_model=ProfileResponse, tags=["Profiles - Update"])
def update_profile_details_by_user_id(user_id:int, profile:ProfileUpdate, db:Session = Depends(get_db)):
    user_exist = get_user_by_id_db(db, UserById(id=user_id))
    if not user_exist:
        raise HTTPException(status_code=404, detail=f"User id {user_id} does not exist")
    profile = update_profile_details_by_user_id_db(db, UserById(id=user_id), profile)
    if not profile:
        raise HTTPException(status_code=500, detail="Profile not updated")
    return profile


#Delete
@router.delete("/userid/{user_id}", tags=["Profiles - Delete"])
def delete_profile_details_by_user_id(user_id:int, db:Session = Depends(get_db)):
    user_exist = get_user_by_id_db(db, UserById(id=user_id))
    if not user_exist:
        raise HTTPException(status_code=404, detail=f"User id {user_id} does not exist")
    profile_exist = get_profile_by_user_id_db(db, UserById(id=user_id))
    if not profile_exist:
        raise HTTPException(status_code=404, detail="profile does not exist")
    delete_profile_details_by_user_id_db(db, UserById(id=user_id))
    return {"response": f"Profile with user Id {user_id} has been deleted successfully"}

@router.delete("/profileid/{profile_id}", tags=["Profiles - Delete"])
def delete_profile_details_by_profile_id(profile_id:int, db:Session = Depends(get_db)):
    profile_exist = get_profile_by_profile_id_db(db, ProfileById(id=profile_id))
    if not profile_exist:
        raise HTTPException(status_code=404, detail=f"Profile id {profile_id} does not exist")
    delete_profile_details_by_profile_id_db(db, ProfileById(id=profile_id))
    return {"response": f"Profile with profile Id {profile_id} has been deleted successfully"}
