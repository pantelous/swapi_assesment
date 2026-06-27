import pytest

from app.modules.character.application.use_case.register_characters import (
    character_from_dict,
    id_from_url,
    register_characters,
)
from app.modules.character.domain.character.entity import Character, CharacterId


def character_payload(**kwargs) -> dict:
    base = {
        "url": "https://swapi.dev/api/people/1/",
        "name": "Luke Skywalker",
        "height": "172",
        "mass": "77",
        "hair_color": "blond",
        "skin_color": "fair",
        "eye_color": "blue",
        "birth_year": "19BBY",
        "gender": "male",
        "homeworld": "https://swapi.dev/api/planets/1/",
        "films": [
            "https://swapi.dev/api/films/1/",
            "https://swapi.dev/api/films/2/",
        ],
    }
    base.update(kwargs)
    return base

class TestIdFromUrl:
    def test_standard_url(self):
        assert id_from_url("https://swapi.dev/api/people/42/") == 42

    def test_url_without_trailing_slash(self):
        assert id_from_url("https://swapi.dev/api/films/3") == 3

    def test_single_segment(self):
        assert id_from_url("7/") == 7

    def test_non_numeric_segment_raises(self):
        with pytest.raises(ValueError, match="Cannot extract ID from URL"):
            id_from_url("https://swapi.dev/api/people/abc/")

    def test_empty_string_raises(self):
        with pytest.raises(ValueError):
            id_from_url("")

class TestCharacterConstruction:
    def test_id_is_derived_from_url(self):
        char = character_from_dict(character_payload(url="https://swapi.dev/api/people/7/"))

        assert char.id == CharacterId(value=7)

    def test_all_fields_mapped(self):
        payload = character_payload()

        char = character_from_dict(payload)

        assert char.name == "Luke Skywalker"
        assert char.height == "172"
        assert char.mass == "77"
        assert char.hair_color == "blond"
        assert char.skin_color == "fair"
        assert char.eye_color == "blue"
        assert char.birth_year == "19BBY"
        assert char.gender == "male"
        assert char.homeworld == "https://swapi.dev/api/planets/1/"
        assert char.swapi_url == "https://swapi.dev/api/people/1/"
        assert char.films == payload["films"]

    def test_optional_fields_absent_default_to_none(self):
        char = character_from_dict({"url": "https://swapi.dev/api/people/5/", "name": "Minimal"})

        assert char.height is None
        assert char.mass is None
        assert char.hair_color is None
        assert char.skin_color is None
        assert char.eye_color is None
        assert char.birth_year is None
        assert char.gender is None
        assert char.homeworld is None

    def test_films_absent_defaults_to_empty_list(self):
        payload = character_payload()
        del payload["films"]

        assert character_from_dict(payload).films == []

    def test_missing_url_raises(self):
        with pytest.raises((ValueError, AttributeError)):
            character_from_dict({"name": "No URL"})

    def test_missing_name_raises(self):
        with pytest.raises(KeyError):
            character_from_dict({"url": "https://swapi.dev/api/people/1/"})

    def test_returns_character_instance(self):
        assert isinstance(character_from_dict(character_payload()), Character)