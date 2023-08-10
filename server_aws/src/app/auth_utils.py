from fastapi import Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException

import os
import jwt
import time
from dotenv import load_dotenv, find_dotenv

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
_ = load_dotenv(find_dotenv())  # read local .env file
JWT_SECRET = os.environ['JWT_SECRET']
JWT_ALGORITHM = 'HS256'


async def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, JWT_SECRET, audience="authenticated", algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except:
        return {}


async def verify_jwt(jwtoken: str) -> bool:
    isTokenValid: bool = False
    try:
        payload = await decodeJWT(jwtoken)
    except:
        payload = None
    if payload:
        isTokenValid = True
    return isTokenValid


async def access_token(req: Request):
    token = await oauth2_scheme(req)
    isTokenValid = await verify_jwt(token)
    if not isTokenValid:
        raise HTTPException(
            status_code=403, detail="Invalid token or expired token.")
    user_auth = await decodeJWT(token)
    user_id = user_auth['sub']
    return token


async def get_user_id(req: Request):
    token = await oauth2_scheme(req)
    user_auth = await decodeJWT(token)
    user_id = user_auth['sub']
    return user_id
