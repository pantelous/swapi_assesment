from datetime import date

import pytest

from app.modules.film.application.use_case.register_films import (
    film_from_dict,
    id_from_url,
    register_films,
)
from app.modules.film.domain.film.entity import Film, FilmId


def film_payload(**kwargs) -> dict:
    base = {
        "url": "https://swapi.dev/api/films/1/",
        "title": "A New Hope",
        "episode_id": 4,
        "opening_crawl": "It is a period of civil war...",
        "director": "George Lucas",
        "producer": "Gary Kurtz, Rick McCallum",
        "release_date": "1977-05-25",
    }
    base.update(kwargs)
    return base

class TestIdFromUrl:
    def test_standard_url(self):
        assert id_from_url("https://swapi.dev/api/films/42/") == 42

    def test_url_without_trailing_slash(self):
        assert id_from_url("https://swapi.dev/api/films/3") == 3

    def test_single_segment(self):
        assert id_from_url("7/") == 7

    def test_non_numeric_segment_raises(self):
        with pytest.raises(ValueError, match="Cannot extract ID from URL"):
            id_from_url("https://swapi.dev/api/films/abc/")

    def test_empty_string_raises(self):
        with pytest.raises(ValueError):
            id_from_url("")



class TestFilmConstruction:
    def test_id_is_derived_from_url(self):
        film = film_from_dict(film_payload(url="https://swapi.dev/api/films/7/"))

        assert film.id == FilmId(value=7)

    def test_all_fields_mapped(self):
        payload = film_payload()

        film = film_from_dict(payload)

        assert film.title == "A New Hope"
        assert film.episode_id == 4
        assert film.opening_crawl == "It is a period of civil war..."
        assert film.director == "George Lucas"
        assert film.producer == "Gary Kurtz, Rick McCallum"
        assert film.release_date == date(1977, 5, 25)
        assert film.swapi_url == "https://swapi.dev/api/films/1/"

    def test_optional_fields_absent_default_to_none(self):
        film = film_from_dict({"url": "https://swapi.dev/api/films/5/", "title": "Minimal", "episode_id": 1})

        assert film.opening_crawl is None
        assert film.director is None
        assert film.producer is None
        assert film.release_date is None

    def test_missing_url_raises(self):
        with pytest.raises((ValueError, AttributeError)):
            film_from_dict({"title": "No URL", "episode_id": 1})

    def test_missing_title_raises(self):
        with pytest.raises(KeyError):
            film_from_dict({"url": "https://swapi.dev/api/films/1/", "episode_id": 4})

    def test_missing_episode_id_raises(self):
        with pytest.raises((KeyError, TypeError)):
            film_from_dict({"url": "https://swapi.dev/api/films/1/", "title": "No Episode"})

    def test_returns_film_instance(self):
        assert isinstance(film_from_dict(film_payload()), Film)

    def test_starships_are_mapped(self):
        payload = film_payload(starships=[
            "https://swapi.dev/api/starships/2/",
            "https://swapi.dev/api/starships/3/",
        ])
        film = film_from_dict(payload)
        assert film.starships == [
            "https://swapi.dev/api/starships/2/",
            "https://swapi.dev/api/starships/3/",
        ]

    def test_starships_absent_defaults_to_empty_list(self):
        payload = film_payload()
        payload.pop("starships", None)
        assert film_from_dict(payload).starships == []
