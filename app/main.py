from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import  OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import jwt
from app.database import get_db, engine, Base
from app import models, schemas, utils

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Intro to SQLAlchemy"}

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/all-users/", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.post("/register", response_model=schemas.UserResponse)
def register_user(email: str, name: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already exists")
    hashed_password = utils.hashed_password(password)
    new_user = models.User(name=name, email=email, password=hashed_password)
    db.add(new_user)
    db.commit()
    return new_user

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    if not utils.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid password")
    
    access_token = utils.create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/profile", response_model=schemas.UserResponse)
def profile(current_user: models.User = Depends(utils.get_current_user)):
    return current_user

@app.post("/update-profile", response_model=schemas.UserResponse)
def update_profile(update_data: schemas.UpdateUser, current_user: models.User = Depends(utils.get_current_user), db: Session = Depends(get_db)):
    if update_data.email:
        existing_user = db.query(models.User).filter(models.User.email == update_data.email).first()
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(status_code=400, detail="Email already exists")
    if update_data.name:
        current_user.name = update_data.name
    if update_data.email:
        current_user.email = update_data.email
    if update_data.password:
        current_user.password = utils.hashed_password(update_data.password)
    
    db.commit()
    db.refresh(current_user)
    return current_user

@app.post("/change-password")
def change_password(data: schemas.ChangePassword, current_user: models.User = Depends(utils.get_current_user), db: Session = Depends(get_db)):
    if not utils.verify_password(data.old_password, current_user.password):
        raise HTTPException(status_code=400, detail="Invalid old password")
    current_user.password = utils.hashed_password(data.new_password)
    db.commit()
    return {"message": "Password changed successfully"}
