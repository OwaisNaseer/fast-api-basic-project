# app/services/user_service.py
"""
Service layer for User domain.
- Implements in-memory CRUD operations and business logic.
- This layer is the right place to add validation rules, hooks, or
  to call repositories/DAOs once a DB is introduced.
- Service functions raise HTTPException so routers can stay thin.
"""

from typing import List
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user_schema import UserCreate

# In-memory data store and id counter.
_users: List[User] = []
_user_id_counter = 1

def _get_next_id() -> int:
    global _user_id_counter
    value = _user_id_counter
    _user_id_counter += 1
    return value

def create_user(payload: UserCreate) -> User:
    """
    Create a new User domain object and append to in-memory store.
    In a DB-backed app, this would call repository/session.add(...) and commit.
    """
    # Example: prevent duplicate emails (simple business rule)
    for u in _users:
        if u.email == payload.email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    user = User(id=_get_next_id(), name=payload.name, email=payload.email)
    _users.append(user)
    return user

def get_users() -> List[User]:
    """Return all users."""
    return _users

def get_user(user_id: int) -> User:
    """Find user by id or raise 404."""
    for u in _users:
        if u.id == user_id:
            return u
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

def update_user(user_id: int, payload: UserCreate) -> User:
    """
    Update existing user.
    - For now we replace the name & email.
    - Add checks as necessary.
    """
    for idx, u in enumerate(_users):
        if u.id == user_id:
            # Prevent email conflicts (optional, demonstrates business logic)
            for other in _users:
                if other.id != user_id and other.email == payload.email:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")

            u.name = payload.name
            u.email = payload.email
            _users[idx] = u
            return u
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

def delete_user(user_id: int) -> dict:
    """Delete user if exists; otherwise raise 404."""
    for u in _users:
        if u.id == user_id:
            _users.remove(u)
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
