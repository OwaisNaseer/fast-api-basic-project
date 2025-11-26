# app/models/user.py
"""
Domain model for User.
- Represents User entity in the application
- Handles conversion between MongoDB documents and domain objects
"""


class User:
    """User domain model."""
    
    def __init__(self, id: str = None, name: str = "", email: str = ""):
        self.id = str(id) if id else None
        self.name = name
        self.email = email
    
    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Create User instance from MongoDB document."""
        _id = data.get("_id")
        return cls(
            id=str(_id) if _id is not None else None,
            name=data.get("name", ""),
            email=data.get("email", "")
        )
    
    def to_dict(self) -> dict:
        """Convert User to dictionary for MongoDB storage."""
        return {"name": self.name, "email": self.email}
