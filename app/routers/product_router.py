# app/routers/product_router.py
"""
HTTP routes for Product domain.
- Parallels the user_router to show consistent structure across domains.
"""

from fastapi import APIRouter
from typing import List

from app.schemas.product_schema import ProductCreate, ProductOut
from app.services.product_service import (
    create_product,
    get_products,
    get_product,
    update_product,
    delete_product,
)

router = APIRouter()

@router.post("/", response_model=ProductOut)
def api_create_product(payload: ProductCreate):
    return create_product(payload)

@router.get("/", response_model=List[ProductOut])
def api_get_products():
    return get_products()

@router.get("/{product_id}", response_model=ProductOut)
def api_get_product(product_id: int):
    return get_product(product_id)

@router.put("/{product_id}", response_model=ProductOut)
def api_update_product(product_id: int, payload: ProductCreate):
    return update_product(product_id, payload)

@router.delete("/{product_id}")
def api_delete_product(product_id: int):
    return delete_product(product_id)
