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
    

def generate_order_by(request_entry: list[str], order_field: OrderField) -> list[OrderBy]:
    """Generate a list of OrderBy objects from request entries."""
    order_by_list = []
    for entry in request_entry:
        parts = entry.split(":")
        field = parts[0]
        direction = OrderDirection.ASC
        if len(parts) > 1 and parts[1].upper() == 'DESC':
            direction = OrderDirection.DESC
        order_by_list.append(OrderBy(field=order_field(field), direction=direction))
    return order_by_list

# class RequestBase(BaseModel):
#     pass

#     @model_validator(mode='before')
#     @classmethod
#     def transform_company_id(cls, request: dict[str, Any]):
#         return request
#         if 'company_id' in request:
#             request['company_id'] = CompanyId(value=request['company_id'])

#         return request

        

        