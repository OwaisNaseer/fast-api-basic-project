# app/models/user.py
"""
Domain model for User.
- This file uses a simple dataclass to represent the domain object in memory.
- When you add a DB later (SQLAlchemy), you would move DB model classes here and
  adapt service layer to return/accept those objects.
"""

from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
    email: str
