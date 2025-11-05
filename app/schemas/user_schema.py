# app/schemas/user_schema.py
"""
Pydantic schemas for User endpoints.
- Request (UserCreate) and Response (UserOut) models.
- Using separate schema names follows best practice: schemas describe API contracts,
  while models describe domain/storage.
"""

from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str 

class UserCreate(UserBase):
    """Schema used when creating/updating a user (request body)"""
    pass

class UserOut(UserBase):
    """Schema returned to clients (response). Includes id."""
    id: int

    class Config:
        orm_mode = True  # helpful when returning ORM objects later
