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


def test_nested_list_to_json_raises_exception_when_nestedList_argument_is_invalid():
    """
    Test an invalid argument such as int to nested_list_to_json
    """
    with pytest.raises(AttributeError) as ex:
        objectUtil.nested_list_to_json(1, [])

    assert (
        ex.value.args[0]
        == "Argument must be a list, invalid argument received '1'."
    )


def test_nested_list_to_json_raises_exception_when_columns_argument_is_invalid():
    """
    Test an invalid argument such as int to nested_list_to_json
    """
    with pytest.raises(AttributeError) as ex:
        objectUtil.nested_list_to_json([], 1)

    assert (
        ex.value.args[0]
        == "Argument must be a list, invalid argument received '1'."
    )


def test_nested_list_to_json_give_json_object_when_nestedList_and_columns_are_provided():
    """
    Test an valid argument for nestedList and columns
    """
    result = objectUtil.nested_list_to_json(
        [
            [1, "sanjeev", "12"],
            [2, "shan", "14"],
            [3, "gibbs", "14"]
        ],
        ["id", "name", "marks"]
    )
    expected = [
        {
            "id": 1,
            "name": "sanjeev",
            "marks": "12"
        },
        {
            "id": 2,
            "name": "shan",
            "marks": "14"
        },
        {
            "id": 3,
            "name": "gibbs",
            "marks": "14"
        }
    ]
    assert(result == expected)
