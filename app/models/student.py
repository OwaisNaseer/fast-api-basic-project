# app/models/student.py
"""
Domain model for Student.
- This file uses a simple dataclass to represent the domain object in memory.
- When you add a DB later (SQLAlchemy), you would move DB model classes here and
  adapt the service layer to return/accept those objects.
"""

from dataclasses import dataclass

@dataclass
class Student:
    id: int
    name: str
    course: str