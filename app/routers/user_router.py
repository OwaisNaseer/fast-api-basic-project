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
async def api_create_user(payload: UserCreate):
    """
    Create a new user.
    - Request body: UserCreate
    - Response model: UserOut (includes id)
    """
    user = await create_user(payload)
    return UserOut(id=user.id, name=user.name, email=user.email)


@router.get("/", response_model=List[UserOut])
async def api_get_users():
    """
    Get list of users.
    - Returns list[UserOut]
    """
    users = await get_users()
    return [UserOut(id=user.id, name=user.name, email=user.email) for user in users]


@router.get("/{user_id}", response_model=UserOut)
async def api_get_user(user_id: str):
    """
    Get a single user by id.
    - Returns 404 if user not found.
    """
    user = await get_user(user_id)
    return UserOut(id=user.id, name=user.name, email=user.email)


@router.put("/{user_id}", response_model=UserOut)
async def api_update_user(user_id: str, payload: UserCreate):
    """
    Update a user.
    - For simplicity we reuse UserCreate schema for update.
    """
    user = await update_user(user_id, payload)
    return UserOut(id=user.id, name=user.name, email=user.email)


@router.delete("/{user_id}")
async def api_delete_user(user_id: str):
    """
    Delete a user.
    - Returns a simple message on success.
    """
    return await delete_user(user_id)
