from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from main import app
from database import Base, get_db
from model import User
from security import hash_password


# --------------------------------------------------
# Test client
# --------------------------------------------------

client = TestClient(app)


# --------------------------------------------------
# Test database
# --------------------------------------------------

TEST_DATABASE_URL = "sqlite:///test_book.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


# --------------------------------------------------
# Clean database before every test
# --------------------------------------------------

@pytest.fixture(autouse=True)
def clean_database():

    # Remove old test data
    Base.metadata.drop_all(bind=test_engine)

    # Recreate tables
    Base.metadata.create_all(bind=test_engine)


# --------------------------------------------------
# Replace FastAPI's real database with test database
# --------------------------------------------------

def override_get_db():

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# --------------------------------------------------
# Create test users
# --------------------------------------------------

@pytest.fixture
def create_test_users():

    db = TestingSessionLocal()

    # Normal user
    normal_user = User(
        username="testuser",
        password_hash=hash_password("password123"),
        role="user"
    )

    # Admin user
    admin_user = User(
        username="adminuser",
        password_hash=hash_password("admin123"),
        role="admin"
    )

    # Add both users
    db.add(normal_user)
    db.add(admin_user)

    # Save them
    db.commit()

    # Close database session
    db.close()


# ==================================================
# Authentication Tests
# ==================================================


def test_login_success(create_test_users):

    # Send correct username and password
    response = client.post(
        "/users/login",
        json={
            "username": "testuser",
            "password": "password123"
        }
    )

    # Login should succeed
    assert response.status_code == 200

    # Get response JSON
    data = response.json()

    # JWT should be returned
    assert "access_token" in data

    # Token type should be bearer
    assert data["token_type"] == "bearer"


def test_login_wrong_password(create_test_users):

    # Use a real username but wrong password
    response = client.post(
        "/users/login",
        json={
            "username": "testuser",
            "password": "wrong-password"
        }
    )

    # Wrong credentials must be rejected
    assert response.status_code == 401


def test_get_me_without_token():

    # No Authorization header
    response = client.get("/users/me")

    # Authentication is required
    assert response.status_code == 401


def test_get_me_invalid_token():

    # Send a fake JWT
    response = client.get(
        "/users/me",
        headers={
            "Authorization": "Bearer this-is-not-a-valid-token"
        }
    )

    # Invalid token must be rejected
    assert response.status_code == 401


# ==================================================
# Authorization Tests
# ==================================================


def test_normal_user_admin_access(create_test_users):

    # Login as normal user
    login_response = client.post(
        "/users/login",
        json={
            "username": "testuser",
            "password": "password123"
        }
    )

    # Login should succeed
    assert login_response.status_code == 200

    # Extract JWT
    token = login_response.json()["access_token"]

    # Try to access admin-only endpoint
    response = client.get(
        "/users/admin",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    # Normal user is authenticated
    # but not authorized
    assert response.status_code == 403


def test_admin_access(create_test_users):

    # Login as admin
    login_response = client.post(
        "/users/login",
        json={
            "username": "adminuser",
            "password": "admin123"
        }
    )

    # Login should succeed
    assert login_response.status_code == 200

    # Extract JWT
    token = login_response.json()["access_token"]

    # Access admin-only endpoint
    response = client.get(
        "/users/admin",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    # Admin should be allowed
    assert response.status_code == 200

    # Check response message
    assert response.json()["message"] == "Welcome Admin"