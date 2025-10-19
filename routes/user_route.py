from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from core.security import verify_access_token
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.user_schema import UserCreate,UserResponse,UserLogin
from controllers.user_controlller import create_user,login_user
from db.models.user_model import User

router = APIRouter(prefix="/user",tags=["Users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/register")
def register_user(user : UserCreate ,db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User already registered!")
    return create_user(user,db)

@router.post("/login")
def login(user : UserLogin,db: Session=Depends(get_db)):
    return login_user(user,db)

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    return payload

@router.get("/me")
def get_profile(current_user : dict = Depends(get_current_user)):
    return {"user" : current_user}
