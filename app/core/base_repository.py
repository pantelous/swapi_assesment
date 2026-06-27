from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

class SqlBaseRepository:
    """Base class for SQL repositories."""

    def __init__(self, session: Session):
        self.session = session
