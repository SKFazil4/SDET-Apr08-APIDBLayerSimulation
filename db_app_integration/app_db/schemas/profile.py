from pydantic import BaseModel

#Create
class ProfileCreate(BaseModel):
    user_id: int
    bio: str


#Read
class ProfileResponse(BaseModel):
    id:int
    user_id:int
    bio:str

class ProfileById(BaseModel):
    id:int


#Update
class ProfileUpdate(BaseModel):
    bio:str