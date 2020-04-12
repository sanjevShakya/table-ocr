import pytest
from .context import objectUtil

def test_is_dict(capsys, example_fixture):
    # pylint: disable=W0612,W0613
    # When
    result = objectUtil.is_dict({})

    assert result == True


def test_dict_to_list_returns_list_when_valid_arguments_is_dict():
    """
    Test a dictionary converted to list.
    """
    value = {
        "foo": "bar",
        "just": "test",
        "hello": "world",
    }

    expected = [
        {"name": "foo", "value": "bar"},
        {"name": "just", "value": "test"},
        {"name": "hello", "value": "world"},
    ]

    assert objectUtil.dict_to_list(value) == expected


def test_dict_to_list_return_dict_with_custom_keys():
    """ Cases of objectUtil.dict_to_list() with custom `keys` """
    items = {"test101.txt": 23, "test201.txt": 24}

    assert objectUtil.dict_to_list(items, "key", "size") == [
        {"key": "test101.txt", "size": 23},
        {"key": "test201.txt", "size": 24},
    ]


def test_dict_to_list_returns_empty_list_when_argument_is_empty_dict():
    """
    Test an empty dictionary converted to empty list.
    """
    assert objectUtil.dict_to_list({}) == []


def test_dict_to_list_raises_exception_when_argument_is_invalid():
    """
    Test an invalid argument such as int to dict_to_list
    """
    with pytest.raises(AttributeError) as ex:
        objectUtil.dict_to_list(1)

    assert (
        ex.value.args[0]
        == "Argument must be a dictionary, invalid argument received '1'."
    )
