from unittest.mock import MagicMock

from app.modules.character.application.use_case.get_characters import (
    GetCharactersQuery,
    get_characters,
)
from app.modules.character.application.use_case.register_characters import register_characters
from app.modules.character.application.use_case.search_characters import (
    SearchCharacterQuery,
    search_characters,
)
from app.modules.character.domain.character.entity import Character


def make_uow():
    uow = MagicMock()
    uow.__enter__ = MagicMock(return_value=uow)
    uow.__exit__ = MagicMock(return_value=False)
    return uow


LUKE_PAYLOAD = {"url": "https://swapi.dev/api/people/1/", "name": "Luke Skywalker"}
LEIA_PAYLOAD = {"url": "https://swapi.dev/api/people/5/", "name": "Leia Organa"}


class TestRegisterCharacters:
    def test_new_character_is_registered_and_returned(self):
        uow = make_uow()
        uow.character_repo.load_character_id.return_value = None

        result = register_characters([LUKE_PAYLOAD], uow)

        uow.character_repo.register_character.assert_called_once()
        assert len(result) == 1
        assert isinstance(result[0], Character)

    def test_existing_character_is_skipped(self):
        uow = make_uow()
        uow.character_repo.load_character_id.return_value = {"id": 1}

        result = register_characters([LUKE_PAYLOAD], uow)

        uow.character_repo.register_character.assert_not_called()
        assert result == []

    def test_empty_input_returns_empty_list(self):
        uow = make_uow()
        assert register_characters([], uow) == []

    def test_mix_of_new_and_existing(self):
        uow = make_uow()
        uow.character_repo.load_character_id.side_effect = [{"id": 1}, None]

        result = register_characters([LUKE_PAYLOAD, LEIA_PAYLOAD], uow)

        assert len(result) == 1
        assert result[0].name == "Leia Organa"


class TestGetCharacters:
    def test_returns_characters_enriched_with_films(self):
        uow = make_uow()
        uow.character_repo.get_characters.return_value = [{"id": 1, "name": "Luke"}]
        uow.character_repo.get_films_for_character.return_value = [{"id": 4, "title": "A New Hope"}]

        result = get_characters(uow, GetCharactersQuery())

        assert len(result) == 1
        assert result[0]["films"] == [{"id": 4, "title": "A New Hope"}]

    def test_empty_repo_returns_empty_list(self):
        uow = make_uow()
        uow.character_repo.get_characters.return_value = []

        result = get_characters(uow, GetCharactersQuery())

        assert result == []

    def test_pagination_params_are_forwarded(self):
        uow = make_uow()
        uow.character_repo.get_characters.return_value = []

        get_characters(uow, GetCharactersQuery(page=3, page_size=5))

        uow.character_repo.get_characters.assert_called_once_with(limit=5, offset=10)


class TestSearchCharacters:
    def test_returns_repo_result(self):
        uow = make_uow()
        uow.character_repo.search_character.return_value = [{"id": 1, "name": "Luke"}]

        result = search_characters(uow, SearchCharacterQuery(name="Luke"))

        assert result == [{"id": 1, "name": "Luke"}]

    def test_search_name_is_forwarded_to_repo(self):
        uow = make_uow()
        uow.character_repo.search_character.return_value = []

        search_characters(uow, SearchCharacterQuery(name="Vader"))

        uow.character_repo.search_character.assert_called_once_with(character_name="Vader")
