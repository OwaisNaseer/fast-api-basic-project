# app/routers/user_router.py
"""
HTTP routes for User domain.
- Uses dependency injection to call service layer functions.
- Keeps route handlers tiny: they validate input, call service, return result.
"""

from fastapi import APIRouter, HTTPException
from typing import List

from app.schemas.user_schema import UserCreate, UserOut
from app.services.user_service import (
    create_user,
    get_users,
    get_user,
    update_user,
    delete_user,
)

router = APIRouter()

@router.post("/", response_model=UserOut)
def api_create_user(payload: UserCreate):
    """
    Create a new user.
    - Request body: UserCreate
    - Response model: UserOut (includes id)
    """
    return create_user(payload)


@router.get("/", response_model=List[UserOut])
def api_get_users():
    """
    Get list of users.
    - Returns list[UserOut]
    """
    return get_users()


@router.get("/{user_id}", response_model=UserOut)
def api_get_user(user_id: int):
    """
    Get a single user by id.
    - Returns 404 if user not found.
    """
    return get_user(user_id)


@router.put("/{user_id}", response_model=UserOut)
def api_update_user(user_id: int, payload: UserCreate):
    """
    Update a user.
    - For simplicity we reuse UserCreate schema for update.
    """
    return update_user(user_id, payload)


@router.delete("/{user_id}")
def api_delete_user(user_id: int):
    """
    Delete a user.
    - Returns a simple message on success.
    """
    return delete_user(user_id)
