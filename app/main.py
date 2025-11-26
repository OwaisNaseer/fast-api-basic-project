# app/main.py
"""
Application entrypoint.
- Creates FastAPI app instance
- Manages MongoDB connection lifecycle
- Includes routers for user and product
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database.connection import connect_to_mongo, close_mongo_connection
from app.routers.user_router import router as user_router
from app.routers.product_router import router as product_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for MongoDB connection."""
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(title="Professional Skeleton (MongoDB)", version="0.1.0", lifespan=lifespan)

# Include routers with prefixes and tags for automatic docs organization.
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(product_router, prefix="/products", tags=["products"])


@app.get("/")
def health():
    """
    Simple root endpoint to verify the app is running.
    In real apps you might return app metadata or a health-check payload.
    """
    return {"status": "ok", "app": "FastAPI Professional Skeleton (MongoDB)"}


@app.get("/health/db")
async def health_db():
    """
    Database health check endpoint.
    Tests MongoDB connection and returns status.
    """
    from app.database.connection import get_database
    from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
    
    try:
        db = get_database()
        # Try a simple operation to verify connection
        await db.command('ping')
        return {
            "status": "healthy",
            "database": db.name,
            "message": "MongoDB connection is working"
        }
    except (ServerSelectionTimeoutError, ConnectionFailure) as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "message": "Cannot connect to MongoDB. Please check your connection string, IP whitelist, and network settings."
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Database check failed"
        }