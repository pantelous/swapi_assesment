from datetime import date

from app.modules.film.domain.film.entity import Film, FilmId
from app.modules.film.infrastructure.persistance.sql_queries.film_query import (
    get_characters_for_film_query,
    get_film_query,
    get_films_paginated_query,
    insert_film_query,
    link_film_starship_query,
    search_films_by_title_query,
    update_film_votes_query,
)

A_NEW_HOPE = Film(
    id=FilmId(value=1),
    title="A New Hope",
    episode_id=4,
    opening_crawl="It is a period of civil war...",
    director="George Lucas",
    producer="Gary Kurtz, Rick McCallum",
    release_date="1977-05-25",
    swapi_url="https://swapi.dev/api/films/1/",
    votes = 1
)


class TestSearchFilmsByTitleQuery:
    def test_title_is_wrapped_with_wildcards(self):
        _, params = search_films_by_title_query("Hope")
        assert params["title"] == "%Hope%"

    def test_returns_query_and_params(self):
        query, params = search_films_by_title_query("Hope")
        assert isinstance(query, str)
        assert isinstance(params, dict)


class TestGetFilmQuery:
    def test_params_contain_film_id(self):
        _, params = get_film_query(1)
        assert params["film_id"] == 1


class TestInsertFilmQuery:
    def test_id_is_unwrapped_value(self):
        _, params = insert_film_query(A_NEW_HOPE)
        assert params["id"] == 1

    def test_all_fields_present_in_params(self):
        _, params = insert_film_query(A_NEW_HOPE)
        assert params["title"] == "A New Hope"
        assert params["episode_id"] == 4
        assert params["opening_crawl"] == "It is a period of civil war..."
        assert params["director"] == "George Lucas"
        assert params["producer"] == "Gary Kurtz, Rick McCallum"
        assert params["release_date"] == date(1977, 5, 25)
        assert params["swapi_url"] == "https://swapi.dev/api/films/1/"

    def test_optional_fields_are_none_when_absent(self):
        minimal = Film(id=FilmId(value=2), title="Minimal", episode_id=1)
        _, params = insert_film_query(minimal)
        assert params["opening_crawl"] is None
        assert params["director"] is None
        assert params["producer"] is None
        assert params["release_date"] is None


class TestGetFilmsPaginatedQuery:
    def test_params_contain_limit_and_offset(self):
        _, params = get_films_paginated_query(5, 10)
        assert params["limit"] == 5
        assert params["offset"] == 10


class TestLinkFilmStarshipQuery:
    def test_params_contain_both_ids(self):
        _, params = link_film_starship_query(1, 9)
        assert params["film_id"] == 1
        assert params["starship_id"] == 9


class TestGetCharactersForFilmQuery:
    def test_params_contain_film_id(self):
        _, params = get_characters_for_film_query(4)
        assert params["film_id"] == 4


class TestUpdateFilmVotesQuery:
    def test_film_id_is_unwrapped_value(self):
        _, params = update_film_votes_query(A_NEW_HOPE)
        assert params["film_id"] == 1

    def test_votes_are_included_in_params(self):
        _, params = update_film_votes_query(A_NEW_HOPE)
        assert params["votes"] == 1

    def test_query_targets_films_table(self):
        query, _ = update_film_votes_query(A_NEW_HOPE)
        assert "films" in query.lower()

    def test_returns_query_and_params(self):
        query, params = update_film_votes_query(A_NEW_HOPE)
        assert isinstance(query, str)
        assert isinstance(params, dict)
