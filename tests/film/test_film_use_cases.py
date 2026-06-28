from unittest.mock import MagicMock

import pytest

from app.core.exception import ApplicationException
from app.modules.film.application.use_case.get_films import GetFilmsQuery, get_films
from app.modules.film.application.use_case.register_films import register_films
from app.modules.film.application.use_case.search_films import SearchFilmQuery, search_films
from app.modules.film.application.use_case.vote_film import VoteFilmQuery, vote_film
from app.modules.film.domain.film.entity import Film, FilmId


def make_uow():
    uow = MagicMock()
    uow.__enter__ = MagicMock(return_value=uow)
    uow.__exit__ = MagicMock(return_value=False)
    return uow


HOPE_PAYLOAD = {
    "url": "https://swapi.dev/api/films/1/",
    "title": "A New Hope",
    "episode_id": 4,
    "characters": ["https://swapi.dev/api/people/1/"],
    "starships": ["https://swapi.dev/api/starships/2/"],
}

EMPIRE_PAYLOAD = {
    "url": "https://swapi.dev/api/films/2/",
    "title": "The Empire Strikes Back",
    "episode_id": 5,
    "characters": [],
    "starships": [],
}


class TestRegisterFilms:
    def test_new_film_is_registered_and_returned(self):
        uow = make_uow()
        uow.film_repo.load_film_id.return_value = None

        result = register_films([HOPE_PAYLOAD], uow)

        uow.film_repo.register_film.assert_called_once()
        assert len(result) == 1
        assert isinstance(result[0], Film)

    def test_existing_film_is_skipped(self):
        uow = make_uow()
        uow.film_repo.load_film_id.return_value = {"id": 1}

        result = register_films([HOPE_PAYLOAD], uow)

        uow.film_repo.register_film.assert_not_called()
        assert result == []

    def test_empty_input_returns_empty_list(self):
        uow = make_uow()
        assert register_films([], uow) == []

    def test_characters_are_linked(self):
        uow = make_uow()
        uow.film_repo.load_film_id.return_value = None

        register_films([HOPE_PAYLOAD], uow)

        uow.character_repo.link_character_film.assert_called_once_with(1, 1)

    def test_starships_are_linked(self):
        uow = make_uow()
        uow.film_repo.load_film_id.return_value = None

        register_films([HOPE_PAYLOAD], uow)

        uow.film_repo.link_film_starship.assert_called_once_with(1, 2)

    def test_mix_of_new_and_existing(self):
        uow = make_uow()
        uow.film_repo.load_film_id.side_effect = [{"id": 1}, None]

        result = register_films([HOPE_PAYLOAD, EMPIRE_PAYLOAD], uow)

        assert len(result) == 1
        assert result[0].title == "The Empire Strikes Back"


class TestGetFilms:
    def test_returns_films_enriched_with_characters(self):
        uow = make_uow()
        uow.film_repo.get_films.return_value = [{"id": 1, "title": "A New Hope"}]
        uow.film_repo.get_characters_for_film.return_value = [{"id": 1, "name": "Luke"}]

        result = get_films(uow, GetFilmsQuery())

        assert len(result) == 1
        assert result[0]["characters"] == [{"id": 1, "name": "Luke"}]

    def test_empty_repo_returns_empty_list(self):
        uow = make_uow()
        uow.film_repo.get_films.return_value = []

        assert get_films(uow, GetFilmsQuery()) == []

    def test_pagination_params_are_forwarded(self):
        uow = make_uow()
        uow.film_repo.get_films.return_value = []

        get_films(uow, GetFilmsQuery(page=2, page_size=5))

        uow.film_repo.get_films.assert_called_once_with(limit=5, offset=5)


class TestSearchFilms:
    def test_returns_repo_result(self):
        uow = make_uow()
        uow.film_repo.search_film.return_value = [{"id": 1, "title": "A New Hope"}]

        result = search_films(uow, SearchFilmQuery(name="Hope"))

        assert result == [{"id": 1, "title": "A New Hope"}]

    def test_search_title_is_forwarded_to_repo(self):
        uow = make_uow()
        uow.film_repo.search_film.return_value = []

        search_films(uow, SearchFilmQuery(name="Empire"))

        uow.film_repo.search_film.assert_called_once_with(title="Empire")


def make_film(votes=None) -> Film:
    return Film(id=FilmId(value=1), title="A New Hope", episode_id=4, votes=votes)


class TestVoteFilm:
    def test_first_vote_sets_votes_to_1(self):
        uow = make_uow()
        uow.film_repo.get_film_by_name.return_value = make_film(votes=None)

        result = vote_film(uow, VoteFilmQuery(name="A New Hope"))

        assert result.votes == 1

    def test_subsequent_vote_increments_votes(self):
        uow = make_uow()
        uow.film_repo.get_film_by_name.return_value = make_film(votes=5)

        result = vote_film(uow, VoteFilmQuery(name="A New Hope"))

        assert result.votes == 6

    def test_update_film_votes_is_called_with_updated_film(self):
        uow = make_uow()
        uow.film_repo.get_film_by_name.return_value = make_film(votes=2)

        vote_film(uow, VoteFilmQuery(name="A New Hope"))

        updated_film = uow.film_repo.update_film_votes.call_args[0][0]
        assert updated_film.votes == 3

    def test_commit_is_called(self):
        uow = make_uow()
        uow.film_repo.get_film_by_name.return_value = make_film()

        vote_film(uow, VoteFilmQuery(name="A New Hope"))

        uow.commit.assert_called_once()

    def test_film_id_is_preserved_after_vote(self):
        uow = make_uow()
        uow.film_repo.get_film_by_name.return_value = make_film()

        result = vote_film(uow, VoteFilmQuery(name="A New Hope"))

        assert result.id == FilmId(value=1)

    def test_film_not_found_raises_application_exception(self):
        uow = make_uow()
        uow.film_repo.get_film_by_name.return_value = None

        with pytest.raises(ApplicationException):
            vote_film(uow, VoteFilmQuery(name="Unknown Film"))
