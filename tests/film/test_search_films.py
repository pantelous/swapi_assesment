import pytest
from pydantic import ValidationError

from app.modules.film.application.use_case.search_films import SearchFilmQuery


class TestSearchFilmQuery:
    def test_valid_title(self):
        q = SearchFilmQuery(name="A New Hope")
        assert q.name == "A New Hope"

    def test_whitespace_only_title_raises(self):
        with pytest.raises(ValidationError, match="Title cannot be empty"):
            SearchFilmQuery(name="   ")

    def test_empty_string_raises(self):
        with pytest.raises(ValidationError, match="Title cannot be empty"):
            SearchFilmQuery(name="")

    def test_title_with_leading_trailing_spaces_is_valid(self):
        q = SearchFilmQuery(name="  Hope  ")
        assert q.name == "  Hope  "
