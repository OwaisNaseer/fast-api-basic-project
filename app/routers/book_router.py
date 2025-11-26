
from fastapi import APIRouter
from typing import List

from app.schemas.book_schema import BookCreate, BookOut
from app.services.book_services import (
    create_book,
    get_books,
    get_book,
    update_book,
    delete_book,
)

router = APIRouter()


@router.post("/", response_model=BookOut)
def api_create_book(payload: BookCreate):
    """Create a new book."""
    return create_book(payload)


@router.get("/", response_model=List[BookOut])
def api_get_books():
    """Get all books."""
    return get_books()


@router.get("/{book_id}", response_model=BookOut)
def api_get_book(book_id: int):
    """Get a single book by ID."""
    return get_book(book_id)


@router.put("/{book_id}", response_model=BookOut)
def api_update_book(book_id: int, payload: BookCreate):
    """Update a book by ID."""
    return update_book(book_id, payload)


@router.delete("/{book_id}")
def api_delete_book(book_id: int):
    """Delete a book by ID."""
    return delete_book(book_id)
