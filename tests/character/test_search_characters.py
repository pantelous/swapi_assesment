import pytest
from pydantic import ValidationError

from app.modules.character.application.use_case.search_characters import SearchCharacterQuery


class TestSearchCharacterQuery:
    def test_valid_name(self):
        q = SearchCharacterQuery(name="Luke")
        assert q.name == "Luke"

    def test_whitespace_only_name_raises(self):
        with pytest.raises(ValidationError, match="Name cannot be empty"):
            SearchCharacterQuery(name="   ")

    def test_empty_string_raises(self):
        with pytest.raises(ValidationError, match="Name cannot be empty"):
            SearchCharacterQuery(name="")

    def test_name_with_leading_trailing_spaces_is_valid(self):
        # strips check is only for all-whitespace; mixed content is fine
        q = SearchCharacterQuery(name="  Luke  ")
        assert q.name == "  Luke  "
