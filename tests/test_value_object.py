import pytest

from app.core.entity_protocol import ValueObjectAbstract


class IntVO(ValueObjectAbstract[int]):
    pass


class StrVO(ValueObjectAbstract[str]):
    pass


class TestValueObjectAbstractInit:
    def test_stores_value(self):
        vo = IntVO(42)
        assert vo.value == 42

    def test_str_returns_string_of_value(self):
        assert str(IntVO(7)) == "7"
        assert str(StrVO("hello")) == "hello"


class TestValueObjectAbstractEquality:
    def test_equal_instances_with_same_value(self):
        assert IntVO(1) == IntVO(1)

    def test_unequal_instances_with_different_value(self):
        assert IntVO(1) != IntVO(2)

    def test_comparing_different_types_raises(self):
        with pytest.raises(ValueError, match="Cannot compare"):
            IntVO(1) == StrVO("1")  # noqa: B015

    def test_comparing_with_plain_int_raises(self):
        with pytest.raises(ValueError, match="Cannot compare"):
            IntVO(1) == 1  # noqa: B015


class TestValueObjectAbstractHashing:
    def test_hash_matches_value_hash(self):
        assert hash(IntVO(5)) == hash(5)

    def test_can_be_used_as_dict_key(self):
        d = {IntVO(1): "a", IntVO(2): "b"}
        assert d[IntVO(1)] == "a"

    def test_same_value_same_hash(self):
        assert hash(IntVO(99)) == hash(IntVO(99))
