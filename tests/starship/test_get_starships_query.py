import pytest
from pydantic import ValidationError

from app.modules.starship.application.use_case.get_starships import GetStarshipsQuery


class TestGetStarshipsQueryDefaults:
    def test_default_page_is_1(self):
        q = GetStarshipsQuery()
        assert q.page == 1

    def test_default_page_size_is_10(self):
        q = GetStarshipsQuery()
        assert q.page_size == 10


class TestGetStarshipsQueryValidation:
    def test_page_zero_raises(self):
        with pytest.raises(ValidationError):
            GetStarshipsQuery(page=0)

    def test_negative_page_raises(self):
        with pytest.raises(ValidationError):
            GetStarshipsQuery(page=-1)

    def test_page_size_zero_raises(self):
        with pytest.raises(ValidationError):
            GetStarshipsQuery(page_size=0)

    def test_page_size_above_max_raises(self):
        with pytest.raises(ValidationError):
            GetStarshipsQuery(page_size=101)

    def test_page_size_at_max_is_valid(self):
        q = GetStarshipsQuery(page_size=100)
        assert q.page_size == 100

    def test_valid_custom_values(self):
        q = GetStarshipsQuery(page=4, page_size=15)
        assert q.page == 4
        assert q.page_size == 15


class TestGetStarshipsQueryOffset:
    def test_first_page_offset_is_zero(self):
        q = GetStarshipsQuery(page=1, page_size=10)
        assert q.offset == 0

    def test_second_page_offset(self):
        q = GetStarshipsQuery(page=2, page_size=10)
        assert q.offset == 10

    def test_third_page_offset(self):
        q = GetStarshipsQuery(page=3, page_size=10)
        assert q.offset == 20

    def test_offset_with_custom_page_size(self):
        q = GetStarshipsQuery(page=3, page_size=20)
        assert q.offset == 40
