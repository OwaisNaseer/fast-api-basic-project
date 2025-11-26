# app/services/student_service.py
"""
Service layer for Student domain.
- Implements in-memory CRUD operations and business logic.
- This layer is the right place to add validation rules, hooks, or
  to call repositories/DAOs once a DB is introduced.
- Service functions raise HTTPException so routers can stay thin.
"""

from typing import List
from fastapi import HTTPException, status

from app.models.student import Student
from app.schemas.student_schema import StudentCreate

# In-memory data store and id counter.
_students: List[Student] = []
_student_id_counter = 1


def _get_next_id() -> int:
    global _student_id_counter
    value = _student_id_counter
    _student_id_counter += 1
    return value


def create_student(payload: StudentCreate) -> Student:
    """
    Create a new Student and append to in-memory store.
    Example validation: prevent duplicate roll numbers or emails.
    """
    for s in _students:
        if s.name == payload.name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student already exists",
            )
        if s.course == payload.course:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="Course already exists",
            )

    student = Student(
        id=_get_next_id(),name=payload.name,course=payload.course,)
    _students.append(student)
    return student


def get_students() -> List[Student]:
    """Return all students."""
    return _students


def get_student(student_id: int) -> Student:
    """Find student by id or raise 404."""
    for s in _students:
        if s.id == student_id:
            return s
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
    )


def update_student(student_id: int, payload: StudentCreate) -> Student:
    """
    Update existing student information.
    """
    for idx, s in enumerate(_students):
        if s.id == student_id:
            # Prevent duplicate email or roll number
            for other in _students:
                if other.id != student_id and other.name == payload.name:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Name already in use",
                    )
                if other.id != student_id and other.course == payload.course:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Course already in use",
                    )

            s.name = payload.name
            s.course = payload.course
            _students[idx] = s
            return s
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
    )


def delete_student(student_id: int) -> dict:
    """Delete student if exists; otherwise raise 404."""
    for s in _students:
        if s.id == student_id:
            _students.remove(s)
            return {"message": "Student deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
    )
