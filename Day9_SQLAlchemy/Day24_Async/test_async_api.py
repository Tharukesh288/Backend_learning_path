import pytest
import pytest_asyncio

from httpx import ASGITransport, AsyncClient

from async_api import app
from database import engine


@pytest_asyncio.fixture(autouse=True)
async def cleanup_database():
    yield
    await engine.dispose()


@pytest.mark.asyncio
async def test_get_books():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:

        response = await client.get("/books")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_create_book():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:

        response = await client.post(
            "/books",
            json={
                "title": "Async Testing",
                "pages": 300,
                "price": 499.99,
                "description": "Testing async FastAPI",
                "author_id": 1
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Async Testing"
    assert data["price"] == 499.99