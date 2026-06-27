from app.modules.starship.domain.starship.entity import Starship, StarshipId
from app.modules.starship.infrastructure.persistance.sql_queries.starship_query import (
    get_films_for_starship_query,
    get_pilots_for_starship_query,
    get_starship_query,
    get_starships_paginated_query,
    insert_starship_query,
    link_starship_character_query,
    link_starship_film_query,
    search_starships_by_name_query,
)

DEATH_STAR = Starship(
    id=StarshipId(value=9),
    name="Death Star",
    model="DS-1 Orbital Battle Station",
    manufacturer="Imperial Department of Military Research",
    cost_in_credits="1000000000000",
    length="120000",
    max_atmosphering_speed="n/a",
    crew="342953",
    passengers="843342",
    cargo_capacity="1000000000000",
    consumables="3 years",
    hyperdrive_rating="4.0",
    mglt="10",
    starship_class="Deep Space Mobile Battlestation",
    swapi_url="https://swapi.dev/api/starships/9/",
)


class TestInsertStarshipQuery:
    def test_id_is_unwrapped_value(self):
        _, params = insert_starship_query(DEATH_STAR)
        assert params["id"] == 9

    def test_all_fields_present_in_params(self):
        _, params = insert_starship_query(DEATH_STAR)
        assert params["name"] == "Death Star"
        assert params["model"] == "DS-1 Orbital Battle Station"
        assert params["manufacturer"] == "Imperial Department of Military Research"
        assert params["cost_in_credits"] == "1000000000000"
        assert params["length"] == "120000"
        assert params["max_atmosphering_speed"] == "n/a"
        assert params["crew"] == "342953"
        assert params["passengers"] == "843342"
        assert params["cargo_capacity"] == "1000000000000"
        assert params["consumables"] == "3 years"
        assert params["hyperdrive_rating"] == "4.0"
        assert params["mglt"] == "10"
        assert params["starship_class"] == "Deep Space Mobile Battlestation"
        assert params["swapi_url"] == "https://swapi.dev/api/starships/9/"

    def test_optional_fields_are_none_when_absent(self):
        minimal = Starship(id=StarshipId(value=2), name="Minimal")
        _, params = insert_starship_query(minimal)
        assert params["model"] is None
        assert params["manufacturer"] is None


class TestGetStarshipQuery:
    def test_params_contain_starship_id(self):
        _, params = get_starship_query(9)
        assert params["starship_id"] == 9


class TestLinkStarshipFilmQuery:
    def test_params_contain_both_ids(self):
        _, params = link_starship_film_query(9, 1)
        assert params["starship_id"] == 9
        assert params["film_id"] == 1


class TestLinkStarshipCharacterQuery:
    def test_params_contain_both_ids(self):
        _, params = link_starship_character_query(9, 1)
        assert params["starship_id"] == 9
        assert params["character_id"] == 1


class TestSearchStarshipsByNameQuery:
    def test_name_is_wrapped_with_wildcards(self):
        _, params = search_starships_by_name_query("Death")
        assert params["name"] == "%Death%"

    def test_returns_query_and_params(self):
        query, params = search_starships_by_name_query("Death")
        assert isinstance(query, str)
        assert isinstance(params, dict)


class TestGetStarshipsPaginatedQuery:
    def test_params_contain_limit_and_offset(self):
        _, params = get_starships_paginated_query(20, 40)
        assert params["limit"] == 20
        assert params["offset"] == 40


class TestGetFilmsForStarshipQuery:
    def test_params_contain_starship_id(self):
        _, params = get_films_for_starship_query(9)
        assert params["starship_id"] == 9


class TestGetPilotsForStarshipQuery:
    def test_params_contain_starship_id(self):
        _, params = get_pilots_for_starship_query(9)
        assert params["starship_id"] == 9
