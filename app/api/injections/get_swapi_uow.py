from app.core.db import SessionLocal
from app.uow.swapi_uow import SqlSwapiUoW


def get_swapi_uow():
    """Dependency that returns a UoW bound to the current SQLAlchemy session."""
    return SqlSwapiUoW(
        session_factory=SessionLocal,
    )
