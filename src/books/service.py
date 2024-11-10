from datetime import datetime
from src.db.models import Book
from sqlmodel import desc, select

from src.books.schemas import BookCreateModel, BookUpdateModel
from sqlmodel.ext.asyncio.session import AsyncSession


class BookService:

    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))

        result = await session.exec(statement)

        return result.all()
    
    async def get_all_books_by_user(self, user_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.user_uid == user_uid)

        result = await session.exec(statement)

        return result.all()


    async def get_book(self, book_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)

        result = await session.exec(statement)
       
        book = result.first()

        if book is None:
            return None
        
        return book

    async def create_book (self, data : BookCreateModel, session: AsyncSession) -> dict:
        book_model_dict = data.model_dump()
        new_book = Book(**book_model_dict)

        new_book.publish_date = datetime.strptime(
            book_model_dict["published_date"], "%Y-%m-%d"
         )
        session.add(new_book)
        
        await session.commit()

        return new_book

