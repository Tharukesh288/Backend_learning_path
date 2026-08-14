import bcrypt
from jose import jwt
from datetime import datetime, timedelta, timezone
from config import SECRET_KEY, ALGORITHM

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from model import User
from database import get_db
from crud import get_user_by_username

def hash_password(password:str):
    password_bytes = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(password_bytes,bcrypt.gensalt())
    return hashed_password.decode("utf_8")

def verify_password(plain_password:str,hashed_password:str):
    plain_password_bytes = plain_password.encode("utf-8")
    hashed_password_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(plain_password_bytes,hashed_password_bytes)
                                             

def create_access_token(data:dict,expires_delta:timedelta):

     # data → information we want to put inside the JWT
     # expires_delta → how long the token should remain valid

    to_encode = data.copy()
    
    # Make a copy of the data
    # Example:
    # {"sub": "1"}
    #
    # We copy it so we don't modify the original dictionary

    expire = datetime.now(timezone.utc) + expires_delta

    # Get current UTC time
    # Add the token's lifetime
    # Example: now + 30 minutes

    to_encode.update({
        "exp":expire
    })

    # Add the expiration time to the JWT payload
    #
    # The payload now looks roughly like:
    # {
    #     "sub": "1",
    #     "exp": expiration_time
    # }

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    # Create the actual JWT
    # to_encode → information inside the token
    # SECRET_KEY → signs the token
    # algorithm → tells JWT how to sign it
    return encoded_jwt

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        # Decode and verify the JWT
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Get user ID from token
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    # Find user in database
    user = db.query(User).filter(
        User.id == int(user_id)
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user