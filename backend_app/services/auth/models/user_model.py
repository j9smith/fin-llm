from pydantic import BaseModel
from sqlalchemy import Table, Column, Integer, String, Boolean 
from sqlalchemy.ext.declarative import declarative_base
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users import schemas

Base = declarative_base()

class UserTable(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)

class UserRead(schemas.BaseUser[int]):
    pass  

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass

class UserDB(schemas.BaseUser[int]):
    pass

