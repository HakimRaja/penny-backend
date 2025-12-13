from datetime import datetime,timedelta
from passlib.context import CryptContext
import jwt
from src.config.settings import settings
from fastapi import HTTPException,status,Depends
from fastapi.security import OAuth2PasswordBearer
import hashlib

pwd_context = CryptContext(schemes=["argon2"],deprecated = "auto")

def hash_password(plain_password:str)->str:
    return pwd_context.hash(plain_password)

def verify_password(plain_password:str,hashed_password:str)->bool:
    return pwd_context.verify(plain_password,hashed_password)

def hash_refresh_token(refresh_token):
    return pwd_context.hash(refresh_token)

def verify_refresh_token_hash(refresh_token,hashed_refresh_token):
    return pwd_context.verify(refresh_token,hashed_refresh_token)

def create_access_token(data: dict):
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


def verify_access_token(token:str):
    try:
        decoded_data = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        if decoded_data.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid access token")
        return decoded_data
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")

def create_refresh_token(data: dict):
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    payload.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token

def verify_refresh_token(token: str):
    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        if decoded.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        return decoded

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Refresh token expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token is invalid")

