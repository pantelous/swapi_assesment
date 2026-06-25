from contextlib import contextmanager
from typing import Annotated, Generator

from fastapi import Depends
from app.core.db import SessionLocal
from sqlalchemy.orm import Session


class SessionManager:
    """
    Handles database sessions for both FastAPI dependencies
    and programmatic usage (repositories, services, scripts).
    """

    @staticmethod
    @contextmanager
    def session_scope() -> Generator[Session]:
        """
        Context-managed session for scripts, background jobs, or domain services.

        Usage:
            with SessionManager.session_scope() as db:
                db.add(obj)
                db.commit()
        """
        db = SessionLocal()
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()


def get_session():
    """FastAPI dependency that provides a database session."""
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


SessionDep = Annotated[Session, Depends(get_session)]

