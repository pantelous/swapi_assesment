from typing import Any, Callable, TypeVar

from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.request import OrderBy


T = TypeVar('T')

def order_by_entry_to_str(order_by: OrderBy, mapper: dict) -> str:
    """Build the ORDER BY clause string."""
    field = mapper.get(order_by.field, order_by.field)
    return f'{field} {order_by.direction}'

def order_by_clause(order_by: list[OrderBy], mapper: dict) -> str:
    return ", ".join([order_by_entry_to_str(order, mapper) for order in order_by])

def list_to_sql_array(values: list[Any]) -> str:
    """Convert a list of values to a SQL array representation."""
    if not values:
        return "NULL"
    formatted_values = ", ".join(f"'{value}'" if isinstance(value, str) else str(value) for value in values)
    return f"({formatted_values})"

def where_in_clause(field_name: str, values: list[Any]) -> str:
    """Generate a SQL WHERE IN clause for the given field and values."""
    #placeholders = ", ".join([f":{field_name}_{i}" for i in range(len(values))])
    ids = ", ".join(str(value) for value in values)
    return f"{field_name} IN ({ids})"

class SqlQuery:
    def __init__(self, session: Session, query: str, params: dict[str, Any] | None = None):
        self.session = session
        self.query = query
        self.params = params or {}


    def aggregate(self) -> Any:
        """Execute the query and return a single value."""
        cursor = self.session.execute(text(self.query)) if not self.params else self.session.execute(text(self.query), self.params)

        row = cursor.fetchone()
        if not row:
            return None
        return row[0]
    
    def persist(self) -> None:
        self.session.execute(text(self.query)) if not self.params else self.session.execute(text(self.query), self.params)
        return
    
    def fetch_one(self, transformer: Callable[[dict[str, Any]], T] | None = None, **transformer_kwargs) -> dict[str, Any] | T | None:
        """Execute the query and fetch a single result."""
        query = text(self.query)
        cursor = self.session.execute(query) if not self.params else self.session.execute(query, self.params)

        row = cursor.fetchone()
        if not row:
            return None
        
        if transformer:
            return transformer(row._asdict(), **transformer_kwargs)
        return row._asdict()
    
    def fetch_all(self, transformer: Callable[[dict[str, Any]], T] | None = None) -> list[dict[str, Any]] | list[T]:
        """Execute the query and fetch all results."""
        cursor = self.session.execute(text(self.query)) if not self.params else self.session.execute(text(self.query), self.params)

        if transformer:
            return [transformer(row._asdict()) for row in cursor]
        return [row._asdict() for row in cursor]

        
