

from typing import List
from fastapi import HTTPException, status

from app.models.book import Book
from app.schemas.book_schema import BookCreate

_books: List[Book] = []
_book_id_counter = 1


def _get_next_id() -> int:
    """Generate and return the next unique book ID."""
    global _book_id_counter
    value = _book_id_counter
    _book_id_counter += 1
    return value


def create_book(payload: BookCreate) -> Book:
    """
    Create a new book and append it to the in-memory list.
    You can add validation here (e.g., year must be positive).
    """
    if payload.year <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Year must be a positive number"
        )

    book = Book(
        id=_get_next_id(),
        title=payload.title,
        author=payload.author,
        year=payload.year
    )
    _books.append(book)
    return book


def get_books() -> List[Book]:
    """Return all books."""
    return _books


def get_book(book_id: int) -> Book:
    """Return a single book by its ID or raise an error if not found."""
    for b in _books:
        if b.id == book_id:
            return b
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )


def update_book(book_id: int, payload: BookCreate) -> Book:
    """Update an existing book by ID."""
    for idx, b in enumerate(_books):
        if b.id == book_id:
            if payload.year <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Year must be a positive number"
                )
            b.title = payload.title
            b.author = payload.author
            b.year = payload.year
            _books[idx] = b
            return b
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )


def delete_book(book_id: int) -> dict:
    """Delete a book by its ID."""
    for b in _books:
        if b.id == book_id:
            _books.remove(b)
            return {"message": "Book deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )
