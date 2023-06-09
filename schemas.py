from pydantic import BaseModel

class UserRequestModel(BaseModel):
    username:str
    email: str
    
class UserResponseModel(BaseModel):
    id: int