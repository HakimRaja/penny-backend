from typing import Optional
from sqlmodel import SQLModel,Field
from enum import Enum
import uuid
from datetime import datetime
from pydantic import EmailStr,validator
import re

class UserRole(str,Enum):
    """Defines the allowed values for the user's role."""
    member = "member"
    admin = "admin"

class User(SQLModel,table=True):
    __tablename__ = "users"
    user_id : uuid.UUID = Field(default_factory=uuid.uuid4,primary_key=True)
    username : str = Field(index=True, unique=True, nullable=False)
    email : EmailStr = Field(index=True, unique=True, nullable=False)
    password : str = Field(nullable=False)
    phone_number : str  = Field(index=True, unique=True, nullable=False)
    role : str = Field(default=UserRole.member,nullable=False)
    created_at : Optional[datetime] = Field(default_factory=datetime.utcnow,nullable=False)
    updated_at : Optional[datetime] = Field(default_factory=datetime.utcnow,sa_column_kwargs={"onupdate": datetime.utcnow},nullable=False)
    deleted_at : Optional[datetime] = Field(default=None)
    is_signed_up : bool = Field(default=True)

    @validator("phone_number")
    def validate_phone_number_format(cls, value):
        """
        Validates the phone number format (e.g., simple 10-digit check).
        
        NOTE: Phone number validation is complex globally. Use a robust library 
        like 'phonenumbers' for production.
        """
        # Example using a simple regular expression (e.g., 10 digits, optional country code)
        phone_regex = r"^\+?\d{10,15}$"  
        
        if not re.fullmatch(phone_regex, value):
            raise ValueError('Phone number must be between 10 and 15 digits, optionally starting with a country code (+).')
        
        return value
    
    @validator("password")
    def validate_password_format(cls,value):
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long.')
        
        return value