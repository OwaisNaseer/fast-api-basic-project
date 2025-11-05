# app/core/security.py
"""
Simple security utilities / placeholders.
- For teaching: we include a stub `get_current_user` dependency to show where
  authentication would fit.
- Currently it returns None or raises an HTTPException if used; later replace
  with real auth (JWT, OAuth2, etc).
"""

from fastapi import Depends, HTTPException, status

def get_current_user(token: str | None = None):
    """
    Placeholder function to represent authentication dependency.
    In route signatures you could use: current_user = Depends(get_current_user)
    For now, we keep it simple — no authentication enforced.
    """
    # Example behavior (disabled): raise if token missing
    # if token is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return None  # Means no user object for now
