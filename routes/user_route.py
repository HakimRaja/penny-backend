from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.user_schema import UserCreate,UserResponse
from controllers.user_controlller import create_user
from db.models.user_model import User

router = APIRouter(prefix="/user",tags=["Users"])

@router.post("/register")
def register_user(user : UserCreate ,db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User already registered!")
    return create_user(user,db)