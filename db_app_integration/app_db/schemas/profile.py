from pydantic import BaseModel

class ProfileResponse(BaseModel):
    id:int
    user_id:int
    bio:str