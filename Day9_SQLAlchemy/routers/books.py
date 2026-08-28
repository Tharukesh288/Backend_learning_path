from fastapi import APIRouter,Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
from model import Book,User
import schemas
import crud
from exceptions import BookNotFoundException

# Creates a router specifically for book-related endpoints
router = APIRouter(prefix="/books",tags=["Books"])

def write_log(message:str):
    with open ("activity.log","a") as file:
        file.write(message + "\n")

@router.get("/")
def get_all_books(
    skip: int = 0,
    limit: int = 10,
    author_id: int | None = None,
    sort_by: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db)
):
    return crud.get_all_book(db, skip, limit,author_id,sort_by,order)

@router.post("/",response_model=schemas.BookResponse)
def add_book(book:schemas.BookCreate, background_tasks:BackgroundTasks, db:Session=Depends(get_db)):
    new_book = crud.create_book(db,book)
    background_tasks.add_task(write_log,f"created book {new_book.title}")
    return new_book

@router.get("/{book_id}",response_model=schemas.BookResponse)
def get_single_book(book_id:int,db:Session=Depends(get_db)):

    book = crud.get_book(db,book_id)

    if book is None:
        raise BookNotFoundException()

    return book

@router.put("/{book_id}",response_model=schemas.BookResponse)
def update_book_endpoint(book_id:int, book_data:schemas.BookCreate, db: Session=Depends(get_db)):

    book = crud.update_book(db,book_id,book_data)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="You can't update the book that is not in there baka"
        )
    return book

@router.delete("/{book_id}")
def delete_book_endpoint(book_id:int,db:Session=Depends(get_db)):

    book = crud.delete_book(db,book_id)

    if book is None:
        raise HTTPException(
            status_code= 404,
            detail="You don't need to delete the book that does not exist dummy"
        )
    return {
        "message":"demolished sussfully"
        }



