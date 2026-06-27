import enum
from typing import Any

from pydantic import BaseModel, model_validator

class OrderDirection(enum.StrEnum):
    ASC = 'asc'
    DESC = 'desc'

class OrderField(enum.StrEnum):
    pass

class OrderBy(BaseModel):
    field: OrderField | str
    direction: OrderDirection
        

        