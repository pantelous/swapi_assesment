import pytest

from app.core.protocol import ValueContainer, get_value


class IntContainer:
    def __init__(self, value: int) -> None:
        self.value = value


class StrContainer:
    def __init__(self, value: str) -> None:
        self.value = value


class TestGetValue:
    def test_returns_int_value(self):
        assert get_value(IntContainer(42)) == 42

    def test_returns_str_value(self):
        assert get_value(StrContainer("hello")) == "hello"

    def test_returns_none_value(self):
        container = IntContainer(0)
        container.value = None
        assert get_value(container) is None

    def test_returns_list_value(self):
        container = IntContainer(0)
        container.value = [1, 2, 3]
        assert get_value(container) == [1, 2, 3]

    def test_structural_typing_no_inheritance_required(self):
        class Arbitrary:
            value = "structural"

        assert get_value(Arbitrary()) == "structural"

    def test_returns_same_object_for_mutable_values(self):
        data = {"key": "val"}
        container = IntContainer(0)
        container.value = data
        assert get_value(container) is data


class TestValueContainerProtocol:
    def test_isinstance_check_raises_without_runtime_checkable(self):
        with pytest.raises(TypeError, match="runtime_checkable"):
            isinstance(IntContainer(1), ValueContainer)

    def test_any_class_with_value_attribute_works_structurally(self):
        class Unrelated:
            value = 99

        assert get_value(Unrelated()) == 99
