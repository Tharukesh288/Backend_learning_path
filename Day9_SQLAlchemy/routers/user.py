from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from exceptions import UserAlreadyExistsException

import schemas
import crud

from database import get_db
from security import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/register")
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    # Check whether username already exists
    existing_user = crud.get_user_by_username(
        db,
        user.username
    )
                 
    if existing_user:
        raise UserAlreadyExistsException()

    # Convert plain password into a secure hash
    password_hash = hash_password(user.password)

    # Save user in database
    new_user = crud.create_user(
        db,
        username=user.username,
        password_hash=password_hash
    )

    return {
        "message": "User created successfully",
        "username": new_user.username
    }

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/login")
def login_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    # Find the user by username
    db_user = crud.get_user_by_username(
        db,
        user.username
    )

    # User doesn't exist
    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    # Check the submitted password against the stored hash
    if not verify_password(
        user.password,
        db_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    # Create JWT payload
    token_data = {
        "sub": str(db_user.id),
        "role": db_user.role
    }

    # Create access token
    access_token = create_access_token(
        data=token_data,
        expires_delta=timedelta(minutes=30)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me")
def get_me(
    current_user = Depends(get_current_user)
):
    return {
        "username": current_user.username,
        "role": current_user.role
    }


@router.get("/admin")
def admin_only(
    current_user = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return {
        "message": "Welcome Admin"
    }