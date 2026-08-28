from sqlalchemy.orm import Session              # A Session is used to communicate with the database.
from model import Book, Author, User                  # Import our ORM model.
from schemas import BookCreate, AuthorCreate    
from sqlalchemy.exc import IntegrityError
# Import the schema used for creating books.
def create_book(db:Session,book:BookCreate):    # Function to insert a new book into the database.
    # Make sure the author exists
    author = db.query(Author).filter(Author.id == book.author_id).first()

    if author is None:
        return None
    # Create the Book object
    new_book = Book(                            # Convert the incoming API data into a SQLAlchemy model object.
        title = book.title,
        author_id = book.author_id,
        pages = book.pages,
        price = book.price
    )

    db.add(new_book)                            # "I want to save this object."
    db.commit()                                     
    db.refresh(new_book)                        # Reload the object from the database.
    return new_book

def get_all_book(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    author_id: int | None = None,
    sort_by: str = "id",
    order: str = "asc"
):
    query = db.query(Book)

    if author_id is not None:
        query = query.filter(Book.author_id == author_id)

    if sort_by == "title":
        column = Book.title
    elif sort_by == "price":
        column = Book.price
    else:
        column = Book.id

    if order == "desc":
        query = query.order_by(column.desc())
    else:
        query = query.order_by(column.asc())

    return query.offset(skip).limit(limit).all()

def get_book(db:Session,book_id:int):
    book = db.query(Book).filter(Book.id == book_id).first()

    return book

def update_book(db:Session,book_id:int,book_data:BookCreate):
    book = db.query(Book).filter(Book.id == book_id).first()

    if book is None:
        return None

    book.title = book_data.title
    book.author_id = book_data.author_id
    book.pages = book_data.pages
    book.price = book_data.price

    db.commit()
    db.refresh(book)

    return book 

def delete_book(db:Session, book_id:int):
    book = db.query(Book).filter(Book.id == book_id).first()

    if book is None:
        return None

    db.delete(book)
    db.commit()

    return True

def create_author(db:Session, author_data:AuthorCreate):
    new_author = Author(
        name = author_data.name
    )

    db.add(new_author)
    db.commit()
    db.refresh(new_author)

    return new_author

def get_author(db:Session, author_id:int):
    author = db.query(Author).filter(Author.id == author_id).first()

    return author

def get_user_by_username(db:Session,username:str):
    return(db.query(User).filter(User.username == username).first())

def create_user(db:Session,username:str,password_hash:str):
    new_user =  User(username=username,password_hash=password_hash)

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise

