from sqlmodel import SQLModel, Field, Column , Relationship
import uuid  
from datetime import date, datetime 
import sqlalchemy.dialects.postgresql as pg
from typing import Optional, List

class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(
        sa_column =Column
        (
            pg.UUID,
            nullable = False,
            primary_key = True,
            default = uuid.uuid4
        )
    )
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool = Field(default=False)
    password_hash :str = Field(exclude=True)
    created_at: datetime = Field(sa_column =Column(pg.TIMESTAMP, default = datetime.now))
    update_at: datetime = Field(sa_column = Column(pg.TIMESTAMP, default = datetime.now))
    books: List["Book"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"<User {self.username}>"

class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column =Column
        (
            pg.UUID,
            nullable = False,
            primary_key = True,
            default = uuid.uuid4
        )
    )
    title: str
    author: str
    publisher: str
    publish_date: date   
    page_count: int
    language : str
    created_at: datetime = Field(sa_column =Column(pg.TIMESTAMP, default = datetime.now))
    update_at: datetime = Field(sa_column = Column(pg.TIMESTAMP, default = datetime.now))
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    user: Optional[User] = Relationship(back_populates="books")

    def __repr__(self):
        return f"<Book {self.title}>"

