import pytest
from pydantic import ValidationError

from app.modules.film.application.use_case.get_films import GetFilmsQuery


class TestGetFilmsQueryDefaults:
    def test_default_page_is_1(self):
        q = GetFilmsQuery()
        assert q.page == 1

    def test_default_page_size_is_10(self):
        q = GetFilmsQuery()
        assert q.page_size == 10


class TestGetFilmsQueryValidation:
    def test_page_zero_raises(self):
        with pytest.raises(ValidationError):
            GetFilmsQuery(page=0)

    def test_negative_page_raises(self):
        with pytest.raises(ValidationError):
            GetFilmsQuery(page=-1)

    def test_page_size_zero_raises(self):
        with pytest.raises(ValidationError):
            GetFilmsQuery(page_size=0)

    def test_page_size_above_max_raises(self):
        with pytest.raises(ValidationError):
            GetFilmsQuery(page_size=101)

    def test_page_size_at_max_is_valid(self):
        q = GetFilmsQuery(page_size=100)
        assert q.page_size == 100

    def test_valid_custom_values(self):
        q = GetFilmsQuery(page=2, page_size=5)
        assert q.page == 2
        assert q.page_size == 5


class TestGetFilmsQueryOffset:
    def test_first_page_offset_is_zero(self):
        q = GetFilmsQuery(page=1, page_size=10)
        assert q.offset == 0

    def test_second_page_offset(self):
        q = GetFilmsQuery(page=2, page_size=10)
        assert q.offset == 10

    def test_third_page_offset(self):
        q = GetFilmsQuery(page=3, page_size=10)
        assert q.offset == 20

    def test_offset_with_custom_page_size(self):
        q = GetFilmsQuery(page=3, page_size=20)
        assert q.offset == 40
