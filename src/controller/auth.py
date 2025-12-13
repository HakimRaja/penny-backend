from fastapi import status,HTTPException,Depends
from src.model.user import User
from src.model.refresh_token import RefreshToken
from src.database.connection import get_db_session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.util.auth import hash_password,verify_password,create_access_token,create_refresh_token,hash_refresh_token,verify_refresh_token_hash
from datetime import datetime

async def register_user(user_data,session:AsyncSession):
    try:
        email = await session.exec(select(User.email).where(User.email == user_data.email,User.deleted_at.is_(None)))
        if email.first():
            return HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email already exists")
        phone = await session.exec(select(User.phone_number).where(User.phone_number == user_data.phone_number,User.deleted_at.is_(None)))
        if phone.first():
            return HTTPException(status_code=status.HTTP_409_CONFLICT,detail="phone number already exists")
        username = await session.exec(select(User.username).where(User.username == user_data.username,User.deleted_at.is_(None)))
        if username.first(): 
            return HTTPException(status_code=status.HTTP_409_CONFLICT,detail="username already exists")
        
        db_user = User.model_validate(user_data)
        db_user.password = hash_password(user_data.password)
        payload = {"user_id":str(db_user.user_id),"username" : db_user.username,"email":db_user.email,"phone_number":db_user.phone_number,"role" : db_user.role}
        token = create_access_token(payload)#except password
        refresh_token = create_refresh_token(payload)
        hashed_refresh_token = hash_refresh_token(refresh_token)
        refresh_token_payload = {"user_id" : db_user.user_id , "refresh_token" : hashed_refresh_token}
        db_refresh_token = RefreshToken.model_validate(refresh_token_payload)
    
        #password hashing and jwt token
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        session.add(db_refresh_token)
        await session.commit()
        await session.refresh(db_refresh_token)

        return {
            "message": "User registered successfully",
            "user": {
                "user_id": str(db_user.user_id),  # convert UUID to string
                "username": db_user.username,
                "email": db_user.email,
                "phone_number": db_user.phone_number,
                "role": db_user.role
            },
            "access_token": token,
            "refresh_token" : refresh_token
        }
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Something went wrong!{e}")
    
async def login_user(user_data,session:AsyncSession):
    try:
        result = await session.exec(select(User).where(User.email == user_data.email,User.deleted_at.is_(None)))
        db_user = result.first()
        if not db_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Wrong email or password!")
        if not verify_password(user_data.password,db_user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Wrong email or password!")
        payload = {"user_id":str(db_user.user_id),"username" : db_user.username,"email":db_user.email,"phone_number":db_user.phone_number,"role" : db_user.role}
        token = create_access_token(payload)#except password
        refresh_token = create_refresh_token(payload)
        hashed_refresh_token = hash_refresh_token(refresh_token)
        refresh_token_payload = {"user_id" : db_user.user_id , "refresh_token" : hashed_refresh_token}
        db_refresh_token = RefreshToken.model_validate(refresh_token_payload)
    
        #password hashing and jwt token
        session.add(db_refresh_token)
        await session.commit()
        await session.refresh(db_refresh_token)
        return {
            "message": "User logged in successfully",
            "user": {
                "user_id": str(db_user.user_id),  # convert UUID to string
                "username": db_user.username,
                "email": db_user.email,
                "phone_number": db_user.phone_number,
                "role": db_user.role
            },
            "access_token": token,
            "refresh_token":refresh_token
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Something went wrong!{e}")
    
async def new_access_token(user):
    try:
        token = create_access_token(user.model_dump())

        return {"access_token" : token}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Something went wrong!{e}")
    
async def logout(user,refresh_token,session  :AsyncSession):
    try:

        # 1. Fetch all active refresh tokens for this user
        query = select(RefreshToken).where(
            RefreshToken.user_id == user.user_id,
            RefreshToken.deleted_at.is_(None),
            RefreshToken.logged_out == False
        )

        result = await session.exec(query)
        tokens = result.all()

        if not tokens:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No active refresh tokens found"
            )

        matched_token = None

        # 2. Verify provided refresh token against hashed DB token
        for db_token in tokens:
            if verify_refresh_token_hash(refresh_token, db_token.refresh_token):
                matched_token = db_token
                break

        if not matched_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )

        # 3. Mark as logged out
        matched_token.logged_out = True
        matched_token.updated_at = datetime.utcnow()

        session.add(matched_token)
        await session.commit()
        await session.refresh(matched_token)

        return {"message": "Logout successful"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Something went wrong!{e}")