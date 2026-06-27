import pytest
from pydantic import ValidationError

from app.modules.character.application.use_case.get_characters import GetCharactersQuery


class TestGetCharactersQueryDefaults:
    def test_default_page_is_1(self):
        q = GetCharactersQuery()
        assert q.page == 1

    def test_default_page_size_is_10(self):
        q = GetCharactersQuery()
        assert q.page_size == 10


class TestGetCharactersQueryValidation:
    def test_page_zero_raises(self):
        with pytest.raises(ValidationError):
            GetCharactersQuery(page=0)

    def test_negative_page_raises(self):
        with pytest.raises(ValidationError):
            GetCharactersQuery(page=-1)

    def test_page_size_zero_raises(self):
        with pytest.raises(ValidationError):
            GetCharactersQuery(page_size=0)

    def test_page_size_above_max_raises(self):
        with pytest.raises(ValidationError):
            GetCharactersQuery(page_size=101)

    def test_page_size_at_max_is_valid(self):
        q = GetCharactersQuery(page_size=100)
        assert q.page_size == 100

    def test_valid_custom_values(self):
        q = GetCharactersQuery(page=3, page_size=25)
        assert q.page == 3
        assert q.page_size == 25


class TestGetCharactersQueryOffset:
    def test_first_page_offset_is_zero(self):
        q = GetCharactersQuery(page=1, page_size=10)
        assert q.offset == 0

    def test_second_page_offset(self):
        q = GetCharactersQuery(page=2, page_size=10)
        assert q.offset == 10

    def test_third_page_offset(self):
        q = GetCharactersQuery(page=3, page_size=10)
        assert q.offset == 20

    def test_offset_with_custom_page_size(self):
        q = GetCharactersQuery(page=3, page_size=20)
        assert q.offset == 40
