from sqlalchemy.orm import Session
from db.models.user_model import User
from schemas.user_schema import UserCreate,UserLogin
from fastapi import HTTPException,status
from utils.users import get_password_hash,verify_password
from core.security import create_access_token


def create_user(user: UserCreate,db : Session):
    db_user = User(
        first_name = user.first_name,
        last_name = user.last_name,
        email=user.email,
        password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    token = create_access_token({"sub" : str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}

def login_user(user: UserLogin,db:Session):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        result = verify_password(user.password,existing_user.password)
        if result:
            token = create_access_token({"sub" : str(existing_user.id)})
            return {"access_token": token, "token_type": "bearer"} 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Wrong pasword!")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User not found!")