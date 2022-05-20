from jose import JWTError, jwt
from datetime import datetime, timedelta

from app.schemas import *
from app.database import *
from app import models

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

#Import the setting from the Setting class in the config file
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#SECRET_KEY
SECRET_KEY_FASTAPI = settings.secret_key_fastapi

#Algorithm
ALGORITHM = settings.algorithm

#Expiration Time
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY_FASTAPI, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, cred_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY_FASTAPI, ALGORITHM)

        id: str = payload.get("user_id")

        if id is None:
            raise cred_exception

        token_data = TokenData(id = id)

    except JWTError:
        raise cred_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    cred_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail=f"Could not validate credentials",
                                    headers={"WWW-Authenticate":"Bearer"})

    token = verify_access_token(token, cred_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user


