import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app


# ============================================================
# Test Database
# ============================================================

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


# ============================================================
# Database Fixture
# ============================================================

@pytest.fixture(autouse=True)
def db():
    """Create a clean test database for every test."""

    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)


# ============================================================
# FastAPI Database Override
# ============================================================

def override_get_db():
    """Provide FastAPI with a session connected to the test database."""

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db