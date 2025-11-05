# app/core/config.py
"""
Configuration module.
- For now this holds simple constants useful for the app.
- Later this module can read environment variables, handle secrets, or
  provide BaseSettings (Pydantic) for typed config.
"""

from typing import Final

APP_NAME: Final = "FastAPI Professional Skeleton"
APP_VERSION: Final = "0.1.0"

# Example: default pagination limits, placeholder secret, etc.
DEFAULT_PAGE_SIZE: Final = 10
FAKE_SECRET_KEY: Final = "change-me-in-production"
