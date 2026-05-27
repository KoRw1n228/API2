from fastapi import APIRouter, HTTPException, status, Query
from schemas import BookCreate, BookResponse, BookStatus
from services import BookService
from uuid import UUID
from typing import List, Optional

router = APIRouter()
service = BookService()

@router.get("/", response_model=List[BookResponse])
async def get_books(
    author: Optional[str] = None,
    status: Optional[BookStatus] = None,
    sort_by: Optional[str] = Query(None, regex="^(title|year)$")
):
    return await service.list_books(author, status, sort_by)

@router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: UUID):
    book = await service.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книгу не знайдено")
    return book

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def add_book(book: BookCreate):
    return await service.create_book(book)

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID):
    # Ідемпотентний метод: видаляємо і повертаємо 204 незалежно від того, була книга чи ні
    await service.remove_book(book_id)
    return None