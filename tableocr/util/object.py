""" Object utility functions. """

import collections

from typing import Dict

def is_dict(obj):
    """ Check if the object is a dict. """
    return type(obj) == type({})


def dict_to_list(dict: Dict, name_key: str = "name", value_key: str = "value"):
    """
    Returns a list of dictionaries with `name` and `value` keys for all
    key-value pair in given dictionary.
    """
    if not is_dict(dict):
        raise AttributeError(
            "Argument must be a dictionary, invalid argument received '{}'.".format(
                dict
            )
        )

    list = []

    for key, val in dict.items():
        list.append({name_key: key, value_key: val})

    return list