import sqlite3

def get_connection():
    conn = sqlite3.connect("books.db")  # trying to connect the database named books.db file if it does not exist it creates a new file named books.db
    conn.row_factory = sqlite3.Row      # usually it stores the value as tuples so to retrun as row we use the function called row_factory
    return conn

def create_table():
    conn = get_connection()     # the connection represents the open link to the database
    cursor = conn.cursor()      # the cursor is what actually sends SQL commands through that
    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    pages INTEGER NOT NULL,
    price REAL NOT NULL)
    """)
    conn.commit()
    conn.close()
    
def add_book(book):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(""" 
    INSERT INTO books(title,author,pages,price)
    VALUES (?,?,?,?)
    """, (book.title,book.author,book.pages,book.price))    # we are using "?" and putting data seperately to avoid SQL injection (security reasons)

    conn.commit()
    conn.close()

def get_books():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books")

    books = cursor.fetchall()       # usually the data is got form the query but to get it all you need to use the fetchall function 

    conn.close()

    return books

def get_book(book_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?",(book_id,))

    books = cursor.fetchone()
    conn.close()

    return books

def update_book(book_id,book):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE books
    SET title=?,author=?,pages=?,price=?
    WHERE id = ?
    """,(book.title,book.author,book.pages,book.price,book_id))

    conn.commit()
    conn.close()

def delete_book(book_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    DELETE FROM books
    WHERE id = ?
    """,(book_id))

    conn.commit()
    conn.close()
