from sqlalchemy.orm import Session
from db.models.user_model import User
from schemas.user_schema import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"],deprecated = "auto")

def get_password_hash(password : str):
    return pwd_context.hash(password)

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
    return {"user_id": db_user.id}