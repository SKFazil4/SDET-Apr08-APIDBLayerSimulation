from pydantic import BaseModel

#Create
class OrderCreate(BaseModel):
    user_id:int
    item_name:str
    price:int


#Read
class OrderResponse(BaseModel):
    id:int
    user_id:int
    item_name:str
    price:int

class OrderById(BaseModel):
    id:int


#Update
class OrderUpdate(BaseModel):
    user_id:int
    item_name:str
    price:int