import pytest
from pydantic import ValidationError

from app.modules.starship.application.use_case.search_starships import SearchStarshipQuery


class TestSearchStarshipQuery:
    def test_valid_name(self):
        q = SearchStarshipQuery(name="Death Star")
        assert q.name == "Death Star"

    def test_whitespace_only_name_raises(self):
        with pytest.raises(ValidationError, match="Name cannot be empty"):
            SearchStarshipQuery(name="   ")

    def test_empty_string_raises(self):
        with pytest.raises(ValidationError, match="Name cannot be empty"):
            SearchStarshipQuery(name="")

    def test_name_with_leading_trailing_spaces_is_valid(self):
        q = SearchStarshipQuery(name="  Falcon  ")
        assert q.name == "  Falcon  "
