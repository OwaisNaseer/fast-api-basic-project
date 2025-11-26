from pydantic import BaseModel

class StudentBase(BaseModel):
    name: str
    course: str 

class StudentCreate(StudentBase):
    """Schema used when creating/updating a user (request body)"""
    pass

class StudentOut(StudentBase):
    """Schema returned to clients (response). Includes id."""
    id: int

    class Config:
        orm_mode = True  # helpful when returning ORM objects later
