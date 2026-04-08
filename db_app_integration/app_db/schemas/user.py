from pydantic import BaseModel

class UserByName(BaseModel):
    name:str

class UserByEmail(BaseModel):
    email:str

class UserById(BaseModel):
    id:int

class UserCreate(BaseModel):
    name:str
    email:str

class UserResponse(BaseModel):
    id:int
    name:str
    email:str

class UserWithRelations(BaseModel):
    user_id: int
    bio: str