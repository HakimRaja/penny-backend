from fastapi import APIRouter,HTTPException,status,Depends
from src.schema.auth import RegisterData,LoginData,TokenData
from src.controller.auth import register_user,login_user,new_access_token,logout
from src.service.auth import get_current_user,get_current_user_by_refresh_token,get_refresh_token
from src.database.connection import get_db_session
from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter(prefix="/auth",tags=["Authorization"])

@router.post("/register")
async def register(user_data : RegisterData,session : AsyncSession = Depends(get_db_session)):
    if(len(user_data.password) < 8):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="provide a strong password")
    return await register_user(user_data,session)

@router.post("/login")
async def login(user_data : LoginData,session : AsyncSession = Depends(get_db_session)):
    return await login_user(user_data,session)

@router.post("/refresh")
async def refresh_route(current_user : TokenData = Depends(get_current_user_by_refresh_token),session : AsyncSession = Depends(get_db_session)):
    return await new_access_token(current_user)

@router.post("/logout")
async def log_out_route(current_user : TokenData = Depends(get_current_user_by_refresh_token),refresh_token = Depends(get_refresh_token),session : AsyncSession = Depends(get_db_session)):
    return await logout(current_user,refresh_token,session)

@router.get("/me")
async def verify(current_user : TokenData = Depends(get_current_user)):
    return {"current_user" : current_user}