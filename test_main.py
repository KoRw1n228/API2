import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_create_and_get_books():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Тест створення
        payload = {"title": "Kobzar", "author": "Shevchenko", "description": "Poetry", "year": 1840}
        response = await ac.post("/books/", json=payload)
        assert response.status_code == 201
        book_id = response.json()["id"]

        # Тест отримання списку
        response = await ac.get("/books/")
        assert response.status_code == 200
        assert len(response.json()) > 0

        # Тест видалення
        response = await ac.delete(f"/books/{book_id}")
        assert response.status_code == 204