from fastapi import APIRouter,Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
from model import Book,User
import schemas
import crud
from exceptions import BookNotFoundException
from logger import logger

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
    # Log the request and pagination/filter details
    logger.info(
        f"Fetching books | skip={skip}, limit={limit}, "
        f"author_id={author_id}, sort_by={sort_by}, order={order}"
    )

    # Fetch books from the database
    books = crud.get_all_book(
        db, skip, limit, author_id, sort_by, order
    )

    # Log how many books were returned
    logger.info(f"Successfully fetched {len(books)} books")

    # Return the books to the user
    return books

@router.post("/", response_model=schemas.BookResponse)
def add_book(
    book: schemas.BookCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Log that the book creation process has started
    logger.info(f"Creating book: {book.title}")

    try:
        # Try to create the book in the database
        new_book = crud.create_book(db, book)

    except Exception:
        # Log the error AND the full traceback
        logger.exception("Unexpected error while creating book")

        # Re-raise the original exception
        # so FastAPI can handle the actual error normally
        raise

    # Log successful book creation
    logger.info(f"Book created successfully: {new_book.title}")

    # Write the activity message in the background
    background_tasks.add_task(
        write_log,
        f"created book {new_book.title}"
    )

    # Return the newly created book
    return new_book

@router.get("/{book_id}", response_model=schemas.BookResponse)
def get_single_book(book_id: int, db: Session = Depends(get_db)):

    # Log that the API is trying to fetch a specific book
    logger.info(f"Fetching book with ID: {book_id}")

    # Get the book from the database
    book = crud.get_book(db, book_id)

    # Check if the requested book exists
    if book is None:

        # Log a warning because the requested resource was not found
        logger.warning(f"Book not found: ID {book_id}")

        # Raise our custom 404 exception
        raise BookNotFoundException()

    # Log successful retrieval of the book
    logger.info(f"Book found: {book.title}")

    # Return the book to the user
    return book

@router.put("/{book_id}", response_model=schemas.BookResponse)
def update_book_endpoint(
    book_id: int,
    book_data: schemas.BookCreate,
    db: Session = Depends(get_db)
):
    # Log that an update request was received
    logger.info(f"Updating book with ID: {book_id}")

    # Update the book in the database
    book = crud.update_book(db, book_id, book_data)

    # Check whether the book exists
    if book is None:
        # Log a warning because the requested book was not found
        logger.warning(f"Cannot update. Book not found: ID {book_id}")

        raise HTTPException(
            status_code=404,
            detail="You can't update the book that is not in there baka"
        )

    # Log successful update
    logger.info(f"Book updated successfully: {book.title}")

    # Return the updated book
    return book

@router.delete("/{book_id}")
def delete_book_endpoint(book_id: int, db: Session = Depends(get_db)):

    # Log that a delete request was received
    logger.info(f"Deleting book with ID: {book_id}")

    # Try to delete the book from the database
    book = crud.delete_book(db, book_id)

    # Check whether the book existed
    if book is None:
        # Log a warning because there was no book to delete
        logger.warning(f"Cannot delete. Book not found: ID {book_id}")

        raise HTTPException(
            status_code=404,
            detail="You don't need to delete the book that does not exist dummy"
        )

    # Log successful deletion
    logger.info(f"Book deleted successfully: ID {book_id}")

    # Return a success response
    return {
        "message": "demolished successfully"
    }
