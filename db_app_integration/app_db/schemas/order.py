from pydantic import BaseModel

class OrderCreate(BaseModel):
    user_id:int
    item_name:str
    price:int

class OrderResponse(BaseModel):
    id:int
    user_id:int
    item_name:str
    price:int