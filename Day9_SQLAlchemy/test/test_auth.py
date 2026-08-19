from fastapi.testclient import TestClient
import pytest

from main import app
from model import User
from security import hash_password


# ============================================================
# Test Client
# ============================================================

client = TestClient(app)


# ============================================================
# Test Fixtures
# ============================================================

@pytest.fixture
def create_test_users(db):
    """Create a normal user and an admin user for authentication tests."""

    normal_user = User(
        username="testuser",
        password_hash=hash_password("password123"),
        role="user"
    )

    admin_user = User(
        username="adminuser",
        password_hash=hash_password("admin123"),
        role="admin"
    )

    db.add_all([normal_user, admin_user])
    db.commit()


# ============================================================
# Authentication Tests
# ============================================================

def test_login_success(create_test_users):
    """Valid credentials should return a JWT access token."""

    response = client.post(
        "/users/login",
        json={
            "username": "testuser",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(create_test_users):
    """Incorrect password should be rejected."""

    response = client.post(
        "/users/login",
        json={
            "username": "testuser",
            "password": "wrong-password"
        }
    )

    assert response.status_code == 401


def test_login_missing_password():
    """Missing required login fields should return validation error."""

    response = client.post(
        "/users/login",
        json={
            "username": "testuser"
        }
    )

    assert response.status_code == 422


def test_get_me_without_token():
    """Protected endpoint should reject requests without a token."""

    response = client.get("/users/me")

    assert response.status_code == 401


def test_get_me_invalid_token():
    """Protected endpoint should reject an invalid JWT."""

    response = client.get(
        "/users/me",
        headers={
            "Authorization": "Bearer this-is-not-a-valid-token"
        }
    )

    assert response.status_code == 401


# ============================================================
# Authorization Tests
# ============================================================

def test_normal_user_admin_access(create_test_users):
    """Authenticated normal users should not access admin endpoints."""

    login_response = client.post(
        "/users/login",
        json={
            "username": "testuser",
            "password": "password123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/users/admin",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    # User is authenticated but does not have admin permission.
    assert response.status_code == 403


def test_admin_access(create_test_users):
    """Authenticated admin users should access admin endpoints."""

    login_response = client.post(
        "/users/login",
        json={
            "username": "adminuser",
            "password": "admin123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/users/admin",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Welcome Admin"