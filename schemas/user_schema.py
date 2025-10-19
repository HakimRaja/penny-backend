from pydantic import BaseModel,EmailStr

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email : EmailStr
    password : str