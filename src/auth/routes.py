from fastapi import APIRouter, Depends, status
from src.auth.schemas import CreateUserModel, UserModel, LoginUserModel
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import UserService
from src.db.main import get_session
from fastapi.exceptions import HTTPException
from .util import verify_password, generate_token
from datetime import timedelta, datetime
from fastapi.responses import JSONResponse
from .dependencies import RefreshToken, Authorization

auth_router = APIRouter()
auth_service = UserService()
refresh_token_bearer = RefreshToken()
access_token_bearer = Authorization()

REFRESH_TOKEN_EXPIRY = 1

@auth_router.post("/signup", response_model= UserModel, status_code = status.HTTP_201_CREATED)
async def create_user(request: CreateUserModel, session: AsyncSession =  Depends(get_session)):
    user_email = request.email
    user_exists = await auth_service.get_user(user_email, session)
    if user_exists:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already exists")
    
    new_user = await auth_service.create_user(request, session)
    return new_user

@auth_router.post("/login")
async def login_user(login_user: LoginUserModel, session: AsyncSession =  Depends(get_session)):
    user_name = login_user.email
    password = login_user.password

    user = await auth_service.get_user(user_name, session)

    if user is None:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Invalid user credentials")

    
    verified_password = verify_password(password, user.password_hash)
    if verified_password:
        access_token = generate_token(user_data= {
            "user_email": user.email, 
            "user_uid": str(user.uid)
        })

        refresh_token = generate_token(user_data= {
            "user_email": user.email, 
            "user_uid": str(user.uid)
        },refresh_token= True, expiry= timedelta(days= REFRESH_TOKEN_EXPIRY))

        return JSONResponse(content= {
            "message": "User login successfully",
            "access_token": access_token,
            "refresh_token": refresh_token
        })
    else:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Invalid user credentials")

@auth_router.post("/refresh_token")
async def refresh_token(token_details: dict = Depends(refresh_token_bearer)):
    token_expiry = token_details["exp"]

    if datetime.fromtimestamp(token_expiry) > datetime.now() :
        new_access_token = generate_token(user_data= {
            "user_data": token_details["user"]
            
        })

        return JSONResponse(content= {
            "message": "Access token is generate",
            "access_token": new_access_token           
        })
    
    raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= "Invalid or expire token")

@auth_router.get("/profile")
async def get_current_user(token_details : dict = Depends(access_token_bearer),
                            session : AsyncSession = Depends(get_session)):
    print (token_details)
    user_email = token_details['user']['user_email']
    
    current_user = await auth_service.get_user(user_email, sesssion= session)
    if current_user is not None:
        return current_user



