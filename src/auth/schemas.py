from pydantic import BaseModel, Field
import uuid 
from datetime import datetime
from typing import List
from src.books.schemas import Book

class CreateUserModel (BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)

class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    update_at: datetime
    books : List[Book]

class LoginUserModel (BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)