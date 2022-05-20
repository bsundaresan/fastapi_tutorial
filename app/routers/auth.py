from fastapi import FastAPI, status, Depends, APIRouter, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.database import *
from app.schemas import *
from app import models
from app.utils import *
from app.oauth2 import *

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=Token)
def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):

    user = db.query(models.User).filter(models.User.email==user_cred.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials!")

    if not verify(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials!")

    #Create Token and return it
    access_token = create_access_token(data = {"user_id": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
        }
