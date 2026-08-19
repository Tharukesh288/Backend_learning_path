from fastapi.testclient import TestClient

from main import app
from model import Author


# ============================================================
# Test Client
# ============================================================

client = TestClient(app)


# ============================================================
# Book API Tests
# ============================================================

def test_get_book(db):
    """GET /books should return a successful response."""

    response = client.get("/books")

    assert response.status_code == 200


def test_create_book(db):
    """POST /books should create a new book."""

    # Book requires a valid author_id, so create an author first.
    author = Author(name="Test Author")

    db.add(author)
    db.commit()
    db.refresh(author)

    book = {
        "title": "Test Book",
        "author_id": author.id,
        "pages": 300,
        "price": 500
    }

    response = client.post(
        "/books/",
        json=book
    )

    assert response.status_code == 200


def test_get_book_by_id(db):
    """GET /books/{id} should return the requested book."""

    author = Author(name="Test Author")

    db.add(author)
    db.commit()
    db.refresh(author)

    book = {
        "title": "Test Book",
        "author_id": author.id,
        "pages": 300,
        "price": 500
    }

    create_response = client.post(
        "/books/",
        json=book
    )

    assert create_response.status_code == 200

    book_id = create_response.json()["id"]

    response = client.get(f"/books/{book_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Test Book"


def test_get_book_not_found(db):
    """GET /books/{id} should return 404 for a missing book."""

    response = client.get("/books/99999")

    assert response.status_code == 404


def test_create_book_invalid_data(db):
    """Invalid field types should return a validation error."""

    book = {
        "title": "Bad Book",
        "author_id": "abc",
        "pages": 300,
        "price": 500
    }

    response = client.post(
        "/books/",
        json=book
    )

    assert response.status_code == 422


def test_create_book_missing_required_field(db):
    """Missing required fields should return a validation error."""

    book = {
        "author_id": 1,
        "pages": 300,
        "price": 500
    }

    response = client.post(
        "/books/",
        json=book
    )

    assert response.status_code == 422


def test_update_book(db):
    """PUT /books/{id} should update an existing book."""

    author = Author(name="Test Author")

    db.add(author)
    db.commit()
    db.refresh(author)

    original_book = {
        "title": "Original Book",
        "author_id": author.id,
        "pages": 200,
        "price": 300
    }

    create_response = client.post(
        "/books/",
        json=original_book
    )

    assert create_response.status_code == 200

    book_id = create_response.json()["id"]

    updated_book = {
        "title": "Updated Book",
        "author_id": author.id,
        "pages": 500,
        "price": 750
    }

    response = client.put(
        f"/books/{book_id}",
        json=updated_book
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Updated Book"
    assert data["pages"] == 500
    assert data["price"] == 750


def test_update_book_not_found(db):
    """PUT /books/{id} should return 404 for a missing book."""

    updated_book = {
        "title": "Updated Book",
        "author_id": 1,
        "pages": 500,
        "price": 750
    }

    response = client.put(
        "/books/99999",
        json=updated_book
    )

    assert response.status_code == 404


def test_delete_book(db):
    """DELETE /books/{id} should remove an existing book."""

    author = Author(name="Test Author")

    db.add(author)
    db.commit()
    db.refresh(author)

    book = {
        "title": "Book To Delete",
        "author_id": author.id,
        "pages": 200,
        "price": 300
    }

    create_response = client.post(
        "/books/",
        json=book
    )

    assert create_response.status_code == 200

    book_id = create_response.json()["id"]

    response = client.delete(
        f"/books/{book_id}"
    )

    assert response.status_code == 200

    # Verify that the deleted book can no longer be retrieved.
    get_response = client.get(
        f"/books/{book_id}"
    )

    assert get_response.status_code == 404


def test_delete_book_not_found(db):
    """DELETE /books/{id} should return 404 for a missing book."""

    response = client.delete("/books/99999")

    assert response.status_code == 404