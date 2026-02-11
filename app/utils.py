from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "suman"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hashed_password(password: str):
    password_bytes = password.encode("utf-8")[:72] 
    return pwd_context.hash(password_bytes)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email=payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400,detail="Invalid mail")
    except jwt.PyJWTError:
        raise HTTPException(status_code=400,detail="Invalid token")
    
    user=db.query(models.User).filter(models.User.email==email).first()
    if user is None:
        raise HTTPException(status_code=400,detail="User not found")
    return user