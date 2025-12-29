"""
Configuration module for application settings.
"""

from dataclasses import dataclass
from pathlib import Path
from environs import Env

env = Env()

env_file = Path(".env.dev")
if env_file.exists():
    env.read_env(env_file, recurse=False)


@dataclass
class Settings:
    """
    Configuration settings for the application.
    """

    database_url: str


settings = Settings(
    database_url=env.str(
        "DATABASE_URL",
        "postgresql+psycopg2://admin:password@db:5432/web-scraper",
    )
)
