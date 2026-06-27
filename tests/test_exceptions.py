import pytest

from app.core.exception import ApplicationException, DomainException


class TestDomainException:
    def test_is_exception(self):
        assert isinstance(DomainException("oops"), Exception)

    def test_stores_message(self):
        exc = DomainException("something went wrong")
        assert exc.message == "something went wrong"

    def test_default_type(self):
        exc = DomainException("oops")
        assert exc.type == "DomainException"

    def test_custom_type(self):
        exc = DomainException("oops", type="ValidationError")
        assert exc.type == "ValidationError"

    def test_field_defaults_to_none(self):
        exc = DomainException("oops")
        assert exc.field is None

    def test_field_stored(self):
        exc = DomainException("too short", field="name")
        assert exc.field == "name"

    def test_error_code_defaults_to_none(self):
        exc = DomainException("oops")
        assert exc.error_code is None

    def test_error_code_stored(self):
        exc = DomainException("not found", error_code=404)
        assert exc.error_code == 404

    def test_str_includes_field_and_message(self):
        exc = DomainException("too short", field="username")
        assert "username" in str(exc)
        assert "too short" in str(exc)

    def test_can_be_raised_and_caught(self):
        with pytest.raises(DomainException) as exc_info:
            raise DomainException("bad input", field="email", error_code=422)
        assert exc_info.value.field == "email"
        assert exc_info.value.error_code == 422


class TestApplicationException:
    def test_is_exception(self):
        assert isinstance(ApplicationException("oops"), Exception)

    def test_stores_message(self):
        exc = ApplicationException("service unavailable")
        assert exc.message == "service unavailable"

    def test_default_type(self):
        exc = ApplicationException("oops")
        assert exc.type == "ApplicationException"

    def test_custom_type(self):
        exc = ApplicationException("oops", type="ServiceError")
        assert exc.type == "ServiceError"

    def test_field_defaults_to_none(self):
        exc = ApplicationException("oops")
        assert exc.field is None

    def test_error_code_defaults_to_none(self):
        exc = ApplicationException("oops")
        assert exc.error_code is None

    def test_str_includes_field_and_message(self):
        exc = ApplicationException("conflict", field="id")
        assert "id" in str(exc)
        assert "conflict" in str(exc)

    def test_can_be_raised_and_caught(self):
        with pytest.raises(ApplicationException) as exc_info:
            raise ApplicationException("not found", field="user", error_code=404)
        assert exc_info.value.message == "not found"

    def test_does_not_catch_domain_exception(self):
        with pytest.raises(DomainException):
            raise DomainException("domain error")
