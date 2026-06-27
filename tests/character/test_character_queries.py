from app.modules.character.domain.character.entity import Character, CharacterId
from app.modules.character.infrastructure.persistance.sql_queries.character_query import (
    get_character_query,
    get_characters_paginated_query,
    get_films_for_character_query,
    insert_character_query,
    link_character_film_query,
    search_characters_by_name_query,
)

LUKE = Character(
    id=CharacterId(value=1),
    name="Luke Skywalker",
    height="172",
    mass="77",
    hair_color="blond",
    skin_color="fair",
    eye_color="blue",
    birth_year="19BBY",
    gender="male",
    homeworld="https://swapi.dev/api/planets/1/",
    swapi_url="https://swapi.dev/api/people/1/",
)


class TestSearchCharactersByNameQuery:
    def test_name_is_wrapped_with_wildcards(self):
        _, params = search_characters_by_name_query("Luke")
        assert params["name"] == "%Luke%"

    def test_returns_query_and_params(self):
        query, params = search_characters_by_name_query("Luke")
        assert isinstance(query, str)
        assert isinstance(params, dict)


class TestInsertCharacterQuery:
    def test_id_is_unwrapped_value(self):
        _, params = insert_character_query(LUKE)
        assert params["id"] == 1

    def test_all_fields_present_in_params(self):
        _, params = insert_character_query(LUKE)
        assert params["name"] == "Luke Skywalker"
        assert params["height"] == "172"
        assert params["mass"] == "77"
        assert params["hair_color"] == "blond"
        assert params["skin_color"] == "fair"
        assert params["eye_color"] == "blue"
        assert params["birth_year"] == "19BBY"
        assert params["gender"] == "male"
        assert params["homeworld"] == "https://swapi.dev/api/planets/1/"
        assert params["swapi_url"] == "https://swapi.dev/api/people/1/"

    def test_optional_fields_are_none_when_absent(self):
        minimal = Character(id=CharacterId(value=2), name="Minimal")
        _, params = insert_character_query(minimal)
        assert params["height"] is None
        assert params["mass"] is None


class TestLinkCharacterFilmQuery:
    def test_params_contain_both_ids(self):
        _, params = link_character_film_query(1, 4)
        assert params["swapi_character_id"] == 1
        assert params["swapi_film_id"] == 4


class TestGetCharacterQuery:
    def test_params_contain_character_id(self):
        _, params = get_character_query(42)
        assert params["character_id"] == 42


class TestGetCharactersPaginatedQuery:
    def test_params_contain_limit_and_offset(self):
        _, params = get_characters_paginated_query(10, 20)
        assert params["limit"] == 10
        assert params["offset"] == 20


class TestGetFilmsForCharacterQuery:
    def test_params_contain_character_id(self):
        _, params = get_films_for_character_query(7)
        assert params["character_id"] == 7
