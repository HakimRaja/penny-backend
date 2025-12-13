from fastapi import HTTPException,status,Depends
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from src.util.auth import verify_access_token,verify_refresh_token,verify_refresh_token_hash
from src.database.connection import get_db_session
from src.schema.auth import TokenData
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.model.refresh_token import RefreshToken
from src.util.auth import hash_refresh_token

security = HTTPBearer()

def get_current_user(credentials:HTTPAuthorizationCredentials = Depends(security)):
    try:
        decoded = verify_access_token(credentials.credentials)
        return TokenData(**decoded)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Something went wrong!")

async def get_current_user_by_refresh_token(credentials:HTTPAuthorizationCredentials = Depends(security),session : AsyncSession = Depends(get_db_session)):
    try:
        query = select(RefreshToken).where(RefreshToken.deleted_at.is_(None),RefreshToken.logged_out == False)
        decoded = verify_refresh_token(credentials.credentials)
        query = query.where(RefreshToken.user_id == decoded["user_id"])
        result = (await session.exec(query)).all()

        if not result:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not authorized!")
        valid = False
        for token in result:
            if verify_refresh_token_hash(credentials.credentials,token.refresh_token):
                valid = True
                break
        if(valid):
            return TokenData(**decoded)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not authorized!")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Something went wrong!")
    
def get_refresh_token(credentials : HTTPAuthorizationCredentials = Depends(security)):
    return credentials.credentials