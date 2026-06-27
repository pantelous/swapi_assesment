from unittest.mock import MagicMock

from app.modules.starship.application.use_case.get_starships import (
    GetStarshipsQuery,
    get_starships,
)
from app.modules.starship.application.use_case.register_starships import register_starships
from app.modules.starship.application.use_case.search_starships import (
    SearchStarshipQuery,
    search_starships,
)
from app.modules.starship.domain.starship.entity import Starship


def make_uow():
    uow = MagicMock()
    uow.__enter__ = MagicMock(return_value=uow)
    uow.__exit__ = MagicMock(return_value=False)
    return uow


DEATH_STAR_PAYLOAD = {
    "url": "https://swapi.dev/api/starships/9/",
    "name": "Death Star",
    "pilots": ["https://swapi.dev/api/people/1/"],
}

FALCON_PAYLOAD = {
    "url": "https://swapi.dev/api/starships/10/",
    "name": "Millennium Falcon",
    "pilots": [],
}


class TestRegisterStarships:
    def test_new_starship_is_registered_and_returned(self):
        uow = make_uow()
        uow.starship_repo.load_starship_id.return_value = None

        result = register_starships([DEATH_STAR_PAYLOAD], uow)

        uow.starship_repo.register_starship.assert_called_once()
        assert len(result) == 1
        assert isinstance(result[0], Starship)

    def test_existing_starship_is_skipped(self):
        uow = make_uow()
        uow.starship_repo.load_starship_id.return_value = {"id": 9}

        result = register_starships([DEATH_STAR_PAYLOAD], uow)

        uow.starship_repo.register_starship.assert_not_called()
        assert result == []

    def test_empty_input_returns_empty_list(self):
        uow = make_uow()
        assert register_starships([], uow) == []

    def test_pilots_are_linked(self):
        uow = make_uow()
        uow.starship_repo.load_starship_id.return_value = None

        register_starships([DEATH_STAR_PAYLOAD], uow)

        uow.starship_repo.link_starship_character.assert_called_once_with(9, 1)

    def test_mix_of_new_and_existing(self):
        uow = make_uow()
        uow.starship_repo.load_starship_id.side_effect = [{"id": 9}, None]

        result = register_starships([DEATH_STAR_PAYLOAD, FALCON_PAYLOAD], uow)

        assert len(result) == 1
        assert result[0].name == "Millennium Falcon"


class TestGetStarships:
    def test_returns_starships_enriched_with_films_and_pilots(self):
        uow = make_uow()
        uow.starship_repo.get_starships.return_value = [{"id": 9, "name": "Death Star"}]
        uow.starship_repo.get_films_for_starship.return_value = [{"id": 1, "title": "A New Hope"}]
        uow.starship_repo.get_pilots_for_starship.return_value = [{"id": 1, "name": "Luke"}]

        result = get_starships(uow, GetStarshipsQuery())

        assert len(result) == 1
        assert result[0]["films"] == [{"id": 1, "title": "A New Hope"}]
        assert result[0]["pilots"] == [{"id": 1, "name": "Luke"}]

    def test_empty_repo_returns_empty_list(self):
        uow = make_uow()
        uow.starship_repo.get_starships.return_value = []

        assert get_starships(uow, GetStarshipsQuery()) == []

    def test_pagination_params_are_forwarded(self):
        uow = make_uow()
        uow.starship_repo.get_starships.return_value = []

        get_starships(uow, GetStarshipsQuery(page=2, page_size=15))

        uow.starship_repo.get_starships.assert_called_once_with(limit=15, offset=15)


class TestSearchStarships:
    def test_returns_repo_result(self):
        uow = make_uow()
        uow.starship_repo.search_starship.return_value = [{"id": 9, "name": "Death Star"}]

        result = search_starships(uow, SearchStarshipQuery(name="Death"))

        assert result == [{"id": 9, "name": "Death Star"}]

    def test_search_name_is_forwarded_to_repo(self):
        uow = make_uow()
        uow.starship_repo.search_starship.return_value = []

        search_starships(uow, SearchStarshipQuery(name="Falcon"))

        uow.starship_repo.search_starship.assert_called_once_with(name="Falcon")
