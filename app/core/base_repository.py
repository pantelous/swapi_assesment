from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.db_session import get_session


class SqlBaseRepository:
    """Base class for SQL repositories."""

    def __init__(self, session: Annotated[Session, Depends(get_session)]):
        self.session = session
