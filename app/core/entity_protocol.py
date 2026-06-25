import typing
from typing import Generic, Protocol, TypeVar

from pydantic_core import core_schema

T = TypeVar("T")

class ValueObject(Protocol[T]):
    value: T

class Entity(Protocol):
    id: ValueObject

class ValueObjectAbstract(Generic[T]):
    value: T

    def __init__(self, value: T):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other: ValueObject) -> bool:
        if not isinstance(other, type(self)):
            raise ValueError("Cannot compare object of diferent class")
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return core_schema.no_info_plain_validator_function(
            lambda v: cls(v) if not isinstance(v, cls) else v,
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda v: v.value,
                info_arg=False,
            ),
        )