from sqlalchemy import Column,String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4,unique=True,nullable=False)
    first_name = Column(String(50),nullable=False)
    last_name = Column(String(50),nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=False)