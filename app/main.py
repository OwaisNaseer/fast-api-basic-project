# app/main.py
"""
Application entrypoint.
- Creates FastAPI app instance
- Includes routers for user and product
- Configured so that switching to DB / routers / deps later is straightforward
"""

from fastapi import FastAPI

# Import routers (they are simple APIRouter instances)
from app.routers.user_router import router as user_router
from app.routers.product_router import router as product_router
from app.routers.student_router import router as student_router
from app.routers.book_router import router as book_router

app = FastAPI(title="Professional Skeleton (In-Memory)", version="0.1.0")

# Include routers with prefixes and tags for automatic docs organization.
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(product_router, prefix="/products", tags=["products"])
app.include_router(student_router, prefix="/students", tags=["students"])
app.include_router(book_router, prefix="/books", tags=["books"])



@app.get("/")
def health():
    """
    Simple root endpoint to verify the app is running.
    In real apps you might return app metadata or a health-check payload.
    """
    return {"status": "ok", "app": "FastAPI Professional Skeleton (in-memory)"}
