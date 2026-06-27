from abc import ABC, abstractmethod
from sqlalchemy.orm import Session, sessionmaker

from app.core.db import LazySessionLocal

class BaseUoW(ABC):
    session: Session
    _session_cm = None

    def __init__(self, session_factory: LazySessionLocal):
        self.session_factory = session_factory

    def _open_session(self) -> Session:
        """Open a session via the factory, storing the context manager for proper cleanup."""
        self._session_cm = self.session_factory()
        try:
            return self._session_cm.__enter__()
        except Exception:
            self._session_cm = None
            raise

    def commit(self):
        self.session.commit()

    def rollback(self):
        session = getattr(self, "session", None)
        if session is not None:
            session.rollback()

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._session_cm is not None:
            self._session_cm.__exit__(exc_type, exc_val, exc_tb)
        elif getattr(self, "session", None) is not None:
            if exc_type:
                self.rollback()
            self.session.close()