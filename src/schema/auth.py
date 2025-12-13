from typing import Optional,Literal
from pydantic import BaseModel,EmailStr

class RegisterData(BaseModel):
    username : str
    email : EmailStr
    password : str
    phone_number : str
    # role : Literal["member","admin"]
    class Config:
        json_scheme_extra = {
            "example" : {
                "username" : "john12",
                "email": "john@gmail.com",
                "password":"SecurePass123",
                "phone_number":"+923207642917",
                # "role":"member"
            }
        }

class LoginData(BaseModel):
    email : EmailStr
    password : str
    
    class Config:
        json_scheme_extra = {
            "example" : {
                "email": "john@gmail.com",
                "password":"SecurePass123"
            }
        }

class TokenData(BaseModel):
    user_id : str
    username : str
    email : EmailStr
    phone_number : str
    role : str
    exp : int
    iat : int
    type: str