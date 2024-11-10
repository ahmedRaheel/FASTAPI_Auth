from fastapi import APIRouter, status, Depends 
from fastapi.exceptions import HTTPException
from .schemas import Book, BookCreateModel, BookUpdateModel
from typing import List
from .service import BookService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.dependencies import Authorization

book_routes = APIRouter()
book_service = BookService()
authorization = Authorization()

@book_routes.get("/", response_model = List[Book])
async def get_books(session : AsyncSession = Depends(get_session), user = Depends(authorization)):
   books = await book_service.get_all_books(session)
   return books 


@book_routes.post("/", status_code = status.HTTP_201_CREATED ,response_model = Book)
async def create_book(data: BookCreateModel, session: AsyncSession = Depends(get_session)):
   new_book = await book_service.create_book(data, session)
   return new_book
