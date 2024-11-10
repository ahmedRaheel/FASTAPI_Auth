from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import create_engine , SQLModel
from src.config import Config
from sqlalchemy.orm import sessionmaker

from sqlmodel.ext.asyncio.session import AsyncSession

# Create async engine
async_engine = AsyncEngine(create_engine(
    Config.DATABASE_URL, echo=True
))

# Function to initialize the database
async def init_db():
    async with async_engine.begin() as conn:
        # Run the SQLModel metadata to create tables
        from src.db.models import Book
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    Session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with Session() as session:
        yield session

