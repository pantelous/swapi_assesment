from typing import Optional
from pydantic import BaseModel

from app.core.entity_protocol import ValueObjectAbstract


class CharacterId(ValueObjectAbstract):
    value: int


class Character(BaseModel):
    id: CharacterId
    name: str
    height: Optional[str] = None
    mass: Optional[str] = None
    hair_color: Optional[str] = None
    skin_color: Optional[str] = None
    eye_color: Optional[str] = None
    birth_year: Optional[str] = None
    gender: Optional[str] = None
    homeworld: Optional[str] = None
    swapi_url: Optional[str] = None
    films: list[str] = []
