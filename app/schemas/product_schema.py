# app/schemas/product_schema.py
"""
Pydantic schemas for Product endpoints.
- ProductCreate: request payload for creating/updating a product.
- ProductOut: response payload returned to clients.
"""

from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    price: float

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True
