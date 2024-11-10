from fastapi import FastAPI, status
from src.books.routes import book_routes
from src.auth.routes import auth_router
from src.db.main import init_db
from contextlib import asynccontextmanager
from src.config import Config
from .errors import register_exception_handlers
from .middleware import  register_middleware

@asynccontextmanager
async def life_span(app : FastAPI):    
    print (f'Server is runing ......')    
    yield 
    print(f'Server is stop')


version = "v1"
app = FastAPI(
    title = "Book store", 
    description = "Rest apis ",
    version = version,
    life_span = life_span
)


register_exception_handlers(app)
register_middleware(app)

app.include_router(auth_router, prefix=f"/api/{version}/auth")
app.include_router(book_routes, prefix = f"/api/{version}/books")


