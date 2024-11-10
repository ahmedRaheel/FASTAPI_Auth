from fastapi import Request, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from .util import decode_token
from fastapi.exceptions import HTTPException
from src.errors import (InValidTokenException,                         
                         AccesTokenRequiredException,
                         RefreshTokenRequiredException)

class AuthorizationBase(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        token_credentials = await super().__call__(request)
        
        if token_credentials is None:
            raise InValidTokenException()   
        
        access_token = token_credentials.credentials
     
        token_data = decode_token(token= access_token)
        
        if token_data is None:
            raise InValidTokenException()       
       
        self.validate_token_data(token_data)

        return token_data        
        
    def validate_token(self, token:str) -> bool:  
        return True if token is not None else False
    
    def validate_token_data(self, token_data: dict) -> None:
        raise NotImplementedError("Please implement this method in child class")

class Authorization(AuthorizationBase):

    def validate_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise AccesTokenRequiredException()
        
class RefreshToken(AuthorizationBase):

    def validate_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise RefreshTokenRequiredException()