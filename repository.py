from uuid import uuid4, UUID
from models import books_db

class BookRepository:
    async def get_all(self):
        return books_db

    async def get_by_id(self, book_id: UUID):
        return next((b for b in books_db if b["id"] == book_id), None)

    async def add(self, book_data: dict):
        book_data["id"] = uuid4()
        books_db.append(book_data)
        return book_data

    async def delete(self, book_id: UUID):
        global books_db
        initial_len = len(books_db)
        # Ідемпотентність: просто фільтруємо, якщо ID немає — нічого не змініться, помилки не буде
        books_db = [b for b in books_db if b["id"] != book_id]
        return len(books_db) < initial_len