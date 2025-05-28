"""
Centralised configuration module.

• Uses pydantic-settings (Pydantic v2) to load environment variables.
• Automatically points to the .env file that sits two directories above
  this file (i.e., your project root), so you never hit the
  “SQLALCHEMY_DATABASE_URI missing” error again.
"""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ------------------------------------------------------------------ #
    # Application-wide settings (add more as your project grows)         #
    # ------------------------------------------------------------------ #
    ENVIRONMENT: str = "development"          # dev / prod / staging …
    DEBUG: bool = True                        # toggles verbose logging
    SQLALCHEMY_DATABASE_URI: str              # ← loaded from .env

    # ------------------------------------------------------------------ #
    # pydantic-settings inner config                                     #
    # ------------------------------------------------------------------ #
    class Config:
        # Two levels up from this file → project root → .env
        env_file = Path(__file__).resolve().parents[2] / ".env"
        env_file_encoding = "utf-8"


# ---------------------------------------------------------------------- #
# Singleton-style accessor                                               #
# ---------------------------------------------------------------------- #
@lru_cache()
def get_settings() -> Settings:
    """
    Cached factory – ensures we only parse .env once per process.
    """
    return Settings()


# Convenience import for the rest of the codebase:
settings: Settings = get_settings()
