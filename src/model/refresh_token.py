from typing import Optional
from sqlmodel import SQLModel,Field
import uuid
from datetime import datetime

class RefreshToken(SQLModel,table = True):
    refresh_token_id : uuid.UUID = Field(default_factory=uuid.uuid4,primary_key=True)
    user_id : uuid.UUID = Field(nullable=False,foreign_key="users.user_id")
    refresh_token : str
    ip_address : Optional[str] = None
    logged_out : bool = Field(default=False)
    created_at : datetime = Field(default_factory=datetime.utcnow,nullable=False)
    updated_at : datetime = Field(default_factory=datetime.utcnow,nullable=False,sa_column_kwargs={"onupdate": datetime.utcnow})
    deleted_at : Optional[datetime] = Field(default=None)