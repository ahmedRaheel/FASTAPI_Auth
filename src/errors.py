from typing  import Any, Callable
from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

class BookstoreException (Exception):
    """Base class for exceptions"""
    pass

class AccesTokenRequiredException (BookstoreException):
    """User has provided an invalid or expired access token"""
    pass

class RefreshTokenRequiredException (BookstoreException):
    """User has provided an invalid or expired refresh token"""
    pass

class InValidTokenException (BookstoreException):
    """User has provided an invalid or expired token"""
    pass

class InValidRefreshException (BookstoreException):
    """User has provided an invalid or expired refresh token"""
    pass

class InValidCredentialException (BookstoreException):
    """User has provided an invalid credentials"""
    pass

class InValidBookIdException (BookstoreException):
    """User has provided an invalid book Id"""
    pass

class UserAlreadyExistsException (BookstoreException):
    """User has provided information which is already exists"""
    pass

class UnAuthorizedException (BookstoreException):
    """User has not rights to access the resources"""
    pass

async def create_exception_handler(status_code: int, details : Any) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request:Request, exception: BookstoreException):
        return JSONResponse(content= details, status_code= status_code)
    
    return exception_handler

def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(
         UnAuthorizedException,
         create_exception_handler(
             status_code= status.HTTP_401_UNAUTHORIZED,
             details= "User does not authorized"
         )
    )  

    app.add_exception_handler(
         UserAlreadyExistsException,
         create_exception_handler(
             status_code= status.HTTP_403_FORBIDDEN,
             details= "User with email already exists"
         )
    )   
    
    app.add_exception_handler(
         InValidBookIdException,
         create_exception_handler(
             status_code= status.HTTP_400_BAD_REQUEST,
             details= "No book exists with ID"
         )
    )   

    app.add_exception_handler(
         InValidCredentialException,
         create_exception_handler(
             status_code= status.HTTP_403_FORBIDDEN,
             details= "User credentials are not correct"
         )
    )   

    app.add_exception_handler(
         InValidRefreshException,
         create_exception_handler(
             status_code= status.HTTP_403_FORBIDDEN,
             details= "Refresh token is invalid or expire"
         )
    )   

    app.add_exception_handler(
         InValidTokenException,
         create_exception_handler(
             status_code= status.HTTP_403_FORBIDDEN,
             details= "Token is invalid or expire"
         )
    )   

    app.add_exception_handler(
         AccesTokenRequiredException,
         create_exception_handler(
             status_code= status.HTTP_401_UNAUTHORIZED,
             details= "Token is required"
         )
    )   

    app.add_exception_handler(
         RefreshTokenRequiredException,
         create_exception_handler(
             status_code= status.HTTP_401_UNAUTHORIZED,
             details= "Token is required"
         )
    )   

    @app.exception_handler(500)
    async def internal_server_error(request, exc):
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


    @app.exception_handler(SQLAlchemyError)
    async def database__error(request, exc):
        print(str(exc))
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
             