"""
Module for retrieving values out of heavily nested structures
Entrypoint: `get_nested()`
"""


def _iter_get(obj: any, target: any):
    """
    Searches the given iterable obj for a target value
     - Uses the target value as a key if an iterated item is a dictionary
    Returns the first occurrence of the value
    Raises
    """
    for item in obj:
        # check for direct equality
        if item == target:
            return item

        # look for a list item which is a nested dictionary
        if type(item) == dict and item.get(target) is not None:
            # name of dict is the desired key, return the value
            return item.get(target)

    raise LookupError(f'Target {target} not found in iterable object {obj}')


def get_nested(obj: any, path_str: str, split_str: str = '.'):
    """
    Helper method which attempts to get a nested value from any type implementing a `get` method
    Takes a path string of the form a.b.c where nested key values are separated by a period by default
    The separation value can be passed in as a split string and allows passing other paths like a/b/c
    """
    nested_keys = path_str.split(split_str)
    result = obj
    # iterate over each nested key and extract the value
    for key in nested_keys:
        # attempt to access next key in the given structure
        if type(result) == list:
            tmp = _iter_get(result, key)
        else:
            tmp = result.get(key)

        if tmp is None:
            raise LookupError(f'Key {key} from path {nested_keys} not found in object {obj}')
        result = tmp

    return result
