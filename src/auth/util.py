from passlib.context import CryptContext
from datetime  import datetime, timedelta
from src.config import Config
import jwt
import uuid
import logging

passwd_context = CryptContext(schemes=["bcrypt"])
ACCESS_TOKEN_EXPIRY =3600

def generate_password_hash(password: str) -> str:
    hash = passwd_context.hash(password)

    return hash

def verify_password(password: str, password_hash: str) -> bool:
    return passwd_context.verify(password, password_hash)

def generate_token(user_data: dict, expiry :timedelta = None, refresh_token : bool = False):
    payload = {}
    payload['user']= user_data
    payload["exp"] = datetime.now() + (
        expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    )
    payload['jti'] = str(uuid.uuid4())
    payload["refresh"] = refresh_token 
    token =  jwt.encode(
        payload=payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGO
    )
    return token

def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGO]
        )
        return token_data
    except jwt.PyJWTError as exception:
        logging.exception(exception)
        return None
