"""
Database module for managing SQLAlchemy sessions.
"""

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session

from .config import settings

engine: Engine = create_engine(
    settings.database_url,
    echo=True,
    future=True,
)

session_local: "sessionmaker[Session]" = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    future=True,
)


@contextmanager
def get_session() -> Iterator[Session]:
    """
    Context manager for SQLAlchemy session.
    """

    session: Session = session_local()

    try:
        yield session

        session.commit()
    except Exception:
        session.rollback()

        raise
    finally:
        session.close()
