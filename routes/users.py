from fastapi import APIRouter, HTTPException, status, Depends, Body
from auth.hash_password import HashPassword
from fastapi.security import OAuth2PasswordRequestForm
from auth.jwt_handler import create_access_token
from database.connection import get_session
from models.users import User, TokenResponse
from sqlmodel import select, update, delete

user_router = APIRouter(
    tags=["User"]
)

hash_password = HashPassword()

@user_router.post("/signup", description='Registers a new user')
async def sign_up_new_user(data: User = Body(...), session=Depends(get_session)) -> dict:
    statement = select(User).where(User.email == data.email)
    user=session.exec(statement).all()

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied email already exists"
        )

    hashed_password = hash_password.create_hash(data.password)
    data.password = hashed_password

    session.add(data)
    session.commit()
    session.refresh(data)

    return {
        "message": "User successfully registered!"
    }


@user_router.post("/signin", response_model=TokenResponse)
async def sign_in_user(user: OAuth2PasswordRequestForm = Depends(), session=Depends(get_session)) -> dict:
    statement = select(User).where(User.username == user.username)
    user_exist = session.exec(statement).all()

    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    if not hash_password.verify_hash(user.password, user_exist[0].password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong credentials passed"
        )
    access_token = create_access_token(user_exist[0].email)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }
