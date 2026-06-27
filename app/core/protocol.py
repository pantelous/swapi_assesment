from typing import TypeVar
from typing_extensions import Protocol

T = TypeVar('T')

class ValueContainer(Protocol):
    """Protocol for value containers."""
    value: T

def get_value(value_conatiner: ValueContainer) -> T:
    """Get the value from a value container."""
    return value_conatiner.value
