import pytest

from app.modules.character.application.use_case.register_characters import id_from_url
from app.modules.starship.application.use_case.register_starships import starship_from_dict
from app.modules.starship.domain.starship.entity import Starship, StarshipId


def starship_payload(**kwargs) -> dict:
    base = {
        "url": "https://swapi.dev/api/starships/9/",
        "name": "Death Star",
        "model": "DS-1 Orbital Battle Station",
        "manufacturer": "Imperial Department of Military Research",
        "cost_in_credits": "1000000000000",
        "length": "120000",
        "max_atmosphering_speed": "n/a",
        "crew": "342953",
        "passengers": "843342",
        "cargo_capacity": "1000000000000",
        "consumables": "3 years",
        "hyperdrive_rating": "4.0",
        "MGLT": "10",
        "starship_class": "Deep Space Mobile Battlestation",
        "films": ["https://swapi.dev/api/films/1/"],
        "pilots": [],
    }
    base.update(kwargs)
    return base


class TestIdFromUrl:
    def test_standard_url(self):
        assert id_from_url("https://swapi.dev/api/starships/9/") == 9

    def test_url_without_trailing_slash(self):
        assert id_from_url("https://swapi.dev/api/starships/3") == 3

    def test_single_segment(self):
        assert id_from_url("7/") == 7

    def test_non_numeric_segment_raises(self):
        with pytest.raises(ValueError, match="Cannot extract ID from URL"):
            id_from_url("https://swapi.dev/api/starships/abc/")

    def test_empty_string_raises(self):
        with pytest.raises(ValueError):
            id_from_url("")


class TestStarshipConstruction:
    def test_id_is_derived_from_url(self):
        starship = starship_from_dict(starship_payload(url="https://swapi.dev/api/starships/12/"))
        assert starship.id == StarshipId(value=12)

    def test_all_fields_mapped(self):
        payload = starship_payload()
        starship = starship_from_dict(payload)

        assert starship.name == "Death Star"
        assert starship.model == "DS-1 Orbital Battle Station"
        assert starship.manufacturer == "Imperial Department of Military Research"
        assert starship.cost_in_credits == "1000000000000"
        assert starship.length == "120000"
        assert starship.max_atmosphering_speed == "n/a"
        assert starship.crew == "342953"
        assert starship.passengers == "843342"
        assert starship.cargo_capacity == "1000000000000"
        assert starship.consumables == "3 years"
        assert starship.hyperdrive_rating == "4.0"
        assert starship.mglt == "10"
        assert starship.starship_class == "Deep Space Mobile Battlestation"
        assert starship.swapi_url == "https://swapi.dev/api/starships/9/"

    def test_optional_fields_absent_default_to_none(self):
        starship = starship_from_dict({"url": "https://swapi.dev/api/starships/5/", "name": "Minimal"})

        assert starship.model is None
        assert starship.manufacturer is None
        assert starship.cost_in_credits is None
        assert starship.length is None
        assert starship.max_atmosphering_speed is None
        assert starship.crew is None
        assert starship.passengers is None
        assert starship.cargo_capacity is None
        assert starship.consumables is None
        assert starship.hyperdrive_rating is None
        assert starship.mglt is None
        assert starship.starship_class is None

    def test_films_are_mapped(self):
        payload = starship_payload(films=[
            "https://swapi.dev/api/films/1/",
            "https://swapi.dev/api/films/2/",
        ])
        assert starship_from_dict(payload).films == [
            "https://swapi.dev/api/films/1/",
            "https://swapi.dev/api/films/2/",
        ]

    def test_films_absent_defaults_to_empty_list(self):
        payload = starship_payload()
        payload.pop("films", None)
        assert starship_from_dict(payload).films == []

    def test_pilots_are_mapped(self):
        payload = starship_payload(pilots=[
            "https://swapi.dev/api/people/1/",
            "https://swapi.dev/api/people/13/",
        ])
        assert starship_from_dict(payload).pilots == [
            "https://swapi.dev/api/people/1/",
            "https://swapi.dev/api/people/13/",
        ]

    def test_pilots_absent_defaults_to_empty_list(self):
        payload = starship_payload()
        payload.pop("pilots", None)
        assert starship_from_dict(payload).pilots == []

    def test_missing_url_raises(self):
        with pytest.raises((ValueError, AttributeError)):
            starship_from_dict({"name": "No URL"})

    def test_missing_name_raises(self):
        with pytest.raises(KeyError):
            starship_from_dict({"url": "https://swapi.dev/api/starships/1/"})

    def test_returns_starship_instance(self):
        assert isinstance(starship_from_dict(starship_payload()), Starship)
