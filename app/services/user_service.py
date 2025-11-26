# app/services/user_service.py
"""
Service layer for User domain.
- Implements MongoDB CRUD operations and business logic.
- Service functions raise HTTPException so routers can stay thin.
"""

from typing import List
from fastapi import HTTPException, status
from bson import ObjectId
from bson.errors import InvalidId
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure

from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.database.connection import get_database


async def create_user(payload: UserCreate) -> User:
    """Create a new user in MongoDB."""
    try:
        db = get_database()
    except RuntimeError as e:
        # Database not initialized
        print(f"Database not initialized error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is currently unavailable. Please try again later."
        )
    except Exception as e:
        print(f"Unexpected error getting database: {type(e).__name__}: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is currently unavailable. Please try again later."
        )
    
    try:
        existing = await db.users.find_one({"email": payload.email})
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        result = await db.users.insert_one({"name": payload.name, "email": payload.email})
        user_doc = await db.users.find_one({"_id": result.inserted_id})
        return User.from_dict(user_doc)
    except (ServerSelectionTimeoutError, ConnectionFailure) as e:
        print(f"MongoDB connection error: {type(e).__name__}: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is currently unavailable. Please try again later."
        )
    except HTTPException:
        raise
    except Exception as e:
        # Log the actual error for debugging
        print(f"Error creating user: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the user: {str(e)}"
        )


async def get_users() -> List[User]:
    """Get all users from MongoDB."""
    try:
        db = get_database()
        users = []
        async for doc in db.users.find():
            users.append(User.from_dict(doc))
        return users
    except (ServerSelectionTimeoutError, ConnectionFailure) as e:
        # If database connection fails, return empty list instead of crashing
        # This allows the API to work even if MongoDB is temporarily unavailable
        print(f"Warning: Could not fetch users from database: {e}")
        return []
    except Exception as e:
        # Catch any other unexpected errors and return empty list
        print(f"Warning: Unexpected error fetching users: {e}")
        return []


async def get_user(user_id: str) -> User:
    """Get user by ID from MongoDB."""
    try:
        db = get_database()
        try:
            user_doc = await db.users.find_one({"_id": ObjectId(user_id)})
            if not user_doc:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            return User.from_dict(user_doc)
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID format")
    except (ServerSelectionTimeoutError, ConnectionFailure) as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is currently unavailable. Please try again later."
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching the user: {str(e)}"
        )


async def update_user(user_id: str, payload: UserCreate) -> User:
    """Update user in MongoDB."""
    try:
        db = get_database()
        try:
            existing = await db.users.find_one({"_id": ObjectId(user_id)})
            if not existing:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            email_check = await db.users.find_one({"email": payload.email, "_id": {"$ne": ObjectId(user_id)}})
            if email_check:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
            await db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"name": payload.name, "email": payload.email}})
            updated_doc = await db.users.find_one({"_id": ObjectId(user_id)})
            return User.from_dict(updated_doc)
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID format")
    except (ServerSelectionTimeoutError, ConnectionFailure) as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is currently unavailable. Please try again later."
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the user: {str(e)}"
        )


async def delete_user(user_id: str) -> dict:
    """Delete user from MongoDB."""
    try:
        db = get_database()
        try:
            result = await db.users.delete_one({"_id": ObjectId(user_id)})
            if result.deleted_count == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            return {"message": "User deleted successfully"}
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID format")
    except (ServerSelectionTimeoutError, ConnectionFailure) as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is currently unavailable. Please try again later."
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting the user: {str(e)}"
        )
