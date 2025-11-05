# app/models/product.py
"""
Domain model for Product.
- Simple dataclass similar to User model to demonstrate two separate domains.
- Keeps domain-level responsibilities separate from Pydantic schemas (serialization/validation).
"""

from dataclasses import dataclass

@dataclass
class Product:
    id: int
    name: str
    price: float
