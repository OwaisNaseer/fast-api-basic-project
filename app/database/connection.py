# app/database/connection.py
"""
Database connection module.
- Manages MongoDB connection lifecycle
- Provides database instance for services
"""

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import get_settings

_client: AsyncIOMotorClient = None
_database = None


async def connect_to_mongo() -> None:
    """Establish connection to MongoDB."""
    global _client, _database
    settings = get_settings()
    # Increased timeout for Atlas connections (30 seconds)
    _client = AsyncIOMotorClient(
        settings.mongodb_url, 
        serverSelectionTimeoutMS=30000,
        connectTimeoutMS=30000
    )
    _database = _client[settings.mongodb_db_name]
    try:
        await _client.admin.command('ping')
        print("Successfully connected to MongoDB Atlas")
    except Exception as e:
        # Log warning but allow app to start
        # Connection will be retried when actually used
        # Note: _database is still set so operations can be attempted
        print(f"Warning: Could not ping MongoDB during startup: {e}")
        print("App will start, connection will be established on first use.")


async def close_mongo_connection() -> None:
    """Close MongoDB connection."""
    global _client
    if _client:
        _client.close()


def get_database():
    """Get database instance."""
    if _database is None:
        print("ERROR: Database is None when get_database() is called")
        print(f"Client is None: {_client is None}")
        raise RuntimeError("Database not initialized")
    print(f"Database retrieved: {_database.name}")
    return _database
