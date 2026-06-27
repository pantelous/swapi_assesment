from typing import Optional
from pydantic import BaseModel

from app.core.entity_protocol import ValueObjectAbstract


class FilmId(ValueObjectAbstract):
    value: int


class Film(BaseModel):
    id: FilmId
    title: str
    episode_id: int
    opening_crawl: Optional[str] = None
    director: Optional[str] = None
    producer: Optional[str] = None
    release_date: Optional[str] = None
    swapi_url: Optional[str] = None
