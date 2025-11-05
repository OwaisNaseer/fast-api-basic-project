# app/services/product_service.py
"""
Service layer for Product domain.
- Mirrors the structure and behavior of user_service to demonstrate consistency.
- Keeps simple business logic in-memory so you can easily swap in a DB later.
"""

from typing import List
from fastapi import HTTPException, status

from app.models.product import Product
from app.schemas.product_schema import ProductCreate

_products: List[Product] = []
_product_id_counter = 1

def _get_next_id() -> int:
    global _product_id_counter
    value = _product_id_counter
    _product_id_counter += 1
    return value

def create_product(payload: ProductCreate) -> Product:
    """
    Create product and append to in-memory store.
    You might add validation here (e.g., price > 0).
    """
    if payload.price < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Price must be non-negative")

    product = Product(id=_get_next_id(), name=payload.name, price=payload.price)
    _products.append(product)
    return product

def get_products() -> List[Product]:
    return _products

def get_product(product_id: int) -> Product:
    for p in _products:
        if p.id == product_id:
            return p
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

def update_product(product_id: int, payload: ProductCreate) -> Product:
    for idx, p in enumerate(_products):
        if p.id == product_id:
            if payload.price < 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Price must be non-negative")
            p.name = payload.name
            p.price = payload.price
            _products[idx] = p
            return p
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

def delete_product(product_id: int) -> dict:
    for p in _products:
        if p.id == product_id:
            _products.remove(p)
            return {"message": "Product deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
