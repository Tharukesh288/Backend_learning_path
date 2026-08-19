from fastapi import FastAPI,HTTPException, Depends, Request             # Import FastAPI to create our web application
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from exceptions import BookNotFoundException,AppException
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import jwt, JWTError
from fastapi.middleware.cors import CORSMiddleware
import time 

from routers.user import router as user_router
from routers.books import router as books_router
from routers.user import router as users_router
from schemas import BookCreate, BookResponse, AuthorCreate, AuthorResponse,BookSimpleResponse, AuthorWithBookResponse, UserCreate
from crud import create_book, get_all_book, get_book, update_book, delete_book,create_author, get_author
import crud
from database import Base, engine, get_db    # Import the database engine and Base class
from model import Book,User                 # Import the Book model so SQLAlchemy knows this table exists
from security import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM

app = FastAPI()                         # Create the FastAPI application

@app.exception_handler(AppException)
async def app_exception_handler(
    request: Request,
    exc: AppException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error,
            "message": exc.message,
            "status_code": exc.status_code
        }
    )

Base.metadata.create_all(bind=engine)   # Create all database tables that inherit from Base (only if they don't already exist)
    # Base.metadata contains information about all ORM models.
    # create_all() checks if the tables exist.
    # If they don't exist, SQLAlchemy creates them.
    # If they already exist, nothing happens.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
@app.post("/register")
def register_user(user:UserCreate,db:Session=Depends(get_db)):
    existing_user = crud.get_user_by_username(db,user.username)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User name already exist"
        )

    hashed_password = hash_password(user.password)

    new_user = crud.create_user(db,user.username,hashed_password)

    return {
        "message":"User registerd Successfully",
        "username":new_user.username
    }

@app.post("/login")
def login_user(
    user: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # user → contains username and password submitted through the OAuth2 form
    # db → provides our database session

    db_user = crud.get_user_by_username(
        db,
        user.username
    )
    # Search the database for the username

    if not db_user:
        # If the username doesn't exist, reject the login

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        user.password,
        db_user.password_hash
    ):
        # Compare the entered password with the stored password hash

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        data={"sub": str(db_user.id)},
        expires_delta=timedelta(minutes=30)
    )
    # Create a JWT containing the user's ID
    # The token will expire after 30 minutes

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

def get_current_token(token:str = Depends(oauth2_scheme)):
    # FastAPI calls oauth2_scheme()
    # to extract the JWT from:
    #
    # Authorization: Bearer <JWT>
    #
    # The extracted JWT is stored in `token`
    return token

def get_current_token(token:str=Depends(oauth2_scheme)):

    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
            # Decode the JWT
            #
            # token → JWT received from the client
            # SECRET_KEY → verifies that WE signed the token
            # algorithms → tells JWT which algorithm is allowed
            #
            # If the token is invalid or expired,
            # jwt.decode() will raise an error

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )

    return payload

def get_current_user(payload:dict=Depends(get_current_token),db:Session=Depends(get_db)):
    # payload → decoded JWT payload
    # db → database session

    user_id=payload.get("sub")

    # Get the user's ID from the JWT
    #
    # Remember:
    # When we created the JWT, we stored:
    # {"sub": str(db_user.id)}

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = db.query(User).filter(User.id==int(user_id)).first()
    # Search the database for the user
    # whose ID matches the ID inside the JWT

    if user is None:
        # The token may be valid,
        # but the user might no longer exist
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
    return user

def required_admin(current_user:User=Depends(get_current_user)):

    print("USERNAME:", current_user.username)
    print("ROLE:", current_user.role)

    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return current_user

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(books_router)            # Connect the books router to our FastAPI application
app.include_router(users_router)
app.include_router(user_router)


@app.post("/author",response_model=AuthorResponse)
def create_author_endpoint(author_data:AuthorCreate,db:Session=Depends(get_db)):
    return create_author(db,author_data)

@app.get("/author/{author_id}",response_model=AuthorWithBookResponse)
def get_author_endpoint(author_id:int,db:Session=Depends(get_db)):
    author = get_author(db,author_id)
    if author is None:
        raise HTTPException(
            status_code= 404,
            detail="The person you are searching is dead"
        )
    return author

@app.middleware("http")
async def log_requests(request:Request,call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    print(
        f"{request.method} {request.url.path}"
        f"completed in {process_time:4f}s"
    )

    return response

