from pydantic import BaseModel

from app_db.schemas.order import OrderResponse
from app_db.schemas.profile import ProfileResponse


#Create
class UserCreate(BaseModel):
    name:str
    email:str


#Read
class UserByName(BaseModel):
    name:str

class UserByEmail(BaseModel):
    email:str

class UserById(BaseModel):
    id:int

class UserResponse(BaseModel):
    id:int
    name:str
    email:str


#Update
class UserUpdate(BaseModel):
    name:str
    email:str