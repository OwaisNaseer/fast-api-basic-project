# app/routers/student_router.py
"""
HTTP routes for Student domain.
- Uses dependency injection to call service layer functions.
- Keeps route handlers tiny: they validate input, call service, return result.
"""

from fastapi import APIRouter, HTTPException
from typing import List

from app.schemas.student_schema import StudentCreate, StudentOut
from app.services.student_service import (
    create_student,
    get_students,
    get_student,
    update_student,
    delete_student,
)

router = APIRouter()

@router.post("/", response_model=StudentOut)
def api_create_student(payload: StudentCreate):
    """
    Create a new student.
    - Request body: StudentCreate
    - Response model: StudentOut (includes id)
    """
    return create_student(payload)


@router.get("/", response_model=List[StudentOut])
def api_get_students():
    """
    Get list of students.
    - Returns list[StudentOut]
    """
    return get_students()


@router.get("/{student_id}", response_model=StudentOut)
def api_get_student(student_id: int):
    """
    Get a single student by id.
    - Returns 404 if student not found.
    """
    return get_student(student_id)


@router.put("/{student_id}", response_model=StudentOut)
def api_update_student(student_id: int, payload: StudentCreate):
    """
    Update a student.
    - For simplicity we reuse StudentCreate schema for update.
    """
    return update_student(student_id, payload)


@router.delete("/{student_id}")
def api_delete_student(student_id: int):
    """
    Delete a student.
    - Returns a simple message on success.
    """
    return delete_student(student_id)
