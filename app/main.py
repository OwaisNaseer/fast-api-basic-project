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
