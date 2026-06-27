import pytest

from app.modules.character.domain.character.entity import Character, CharacterId
from app.modules.character.infrastructure.transformers.character_transformers import (
    transform_character_data,
)


FULL_CHARACTER_DATA = {
    "id": 1,
    "name": "Luke Skywalker",
    "height": "172",
    "mass": "77",
    "hair_color": "blond",
    "skin_color": "fair",
    "eye_color": "blue",
    "birth_year": "19BBY",
    "gender": "male",
    "homeworld": "https://swapi.dev/api/planets/1/",
    "swapi_url": "https://swapi.dev/api/people/1/",
    "films": ["https://swapi.dev/api/films/1/", "https://swapi.dev/api/films/2/"],
}


class TestTransformCharacterDataNone:
    def test_returns_none_when_input_is_none(self):
        assert transform_character_data(None) is None


class TestTransformCharacterDataReturnsCharacter:
    def test_returns_character_instance(self):
        result = transform_character_data(FULL_CHARACTER_DATA)
        assert isinstance(result, Character)

    def test_id_is_character_id_with_correct_value(self):
        result = transform_character_data(FULL_CHARACTER_DATA)
        assert isinstance(result.id, CharacterId)
        assert result.id.value == 1

    def test_name_is_mapped(self):
        result = transform_character_data(FULL_CHARACTER_DATA)
        assert result.name == "Luke Skywalker"

    def test_optional_fields_are_mapped(self):
        result = transform_character_data(FULL_CHARACTER_DATA)
        assert result.height == "172"
        assert result.mass == "77"
        assert result.hair_color == "blond"
        assert result.skin_color == "fair"
        assert result.eye_color == "blue"
        assert result.birth_year == "19BBY"
        assert result.gender == "male"
        assert result.homeworld == "https://swapi.dev/api/planets/1/"
        assert result.swapi_url == "https://swapi.dev/api/people/1/"

    def test_films_list_is_mapped(self):
        result = transform_character_data(FULL_CHARACTER_DATA)
        assert result.films == [
            "https://swapi.dev/api/films/1/",
            "https://swapi.dev/api/films/2/",
        ]


class TestTransformCharacterDataDefaults:
    def test_optional_fields_default_to_none_when_absent(self):
        result = transform_character_data({"id": 2, "name": "Unknown"})
        assert result.height is None
        assert result.mass is None
        assert result.hair_color is None
        assert result.skin_color is None
        assert result.eye_color is None
        assert result.birth_year is None
        assert result.gender is None
        assert result.homeworld is None
        assert result.swapi_url is None

    def test_films_defaults_to_empty_list_when_absent(self):
        result = transform_character_data({"id": 2, "name": "Unknown"})
        assert result.films == []

    def test_films_defaults_to_empty_list_when_key_missing(self):
        data = {**FULL_CHARACTER_DATA}
        del data["films"]
        result = transform_character_data(data)
        assert result.films == []
