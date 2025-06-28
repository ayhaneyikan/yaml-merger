#!/usr/bin/env python3

"""
Utility which provides a means for merging complex YAML structures via reference

Structure of YAML reference:
```yaml
$replace#?<sub-field?>: <path-to-file?>#<path-to-object>
```
E.g.,
```yaml
Toplevel:
    SubField: one

$replace: /Toplevel/Subfield

$replace: ./other/file#/structure/in/thatFile
```
"""

from copy import deepcopy
import yaml

# local module imports
import get_nested
import constants


def _read_yaml(file_path: str):
    """
    Read in YAML file from given file path
    """
    with open(file_path, 'r') as file:
        yaml_content = yaml.safe_load(file)
        return yaml_content




def _rec_scan_dict(content_dict: dict, parent_path: list):
    """
    Scans the given YAML dictionary recursively for references
    Takes
     - content_dict | YAML dictionary to be scanned
     - parent_path  | path used to reach the current structure
    Returns: list of detected references in the YAML file
    """
    def _rec_scan_list(content_list: list, parent_path: list):
        """
        Iterates over the given list and delegates reference scanning
        - References must be key: value, i.e., they cannot exist in a list directly
        Takes
        - content_list | YAML list to be scanned
        - parent_path  | path used to reach the current structure
        """
        refs = []
        for item in content_list:
            if type(item) == list:
                refs.extend(_rec_scan_list(item, parent_path + [item]))  # recursively handle list
            elif type(item) == dict:
                # don't extend parent_path, handled in the dict func
                refs.extend(_rec_scan_dict(item, parent_path))  # recursively handle dict
            else:
                print(f'PLEB LIST ITEM: {item}')
        return refs

    refs = []
    # iterate over keys at the top-level of the given YAML
    for key in content_dict.keys():
        # check if key is a reference
        # TODO evaluate if regex is beneficial here
        if key.startswith(constants.REFERENCE_KEY):
            # add ref info to the return list
            refs.append((key, content_dict[key], parent_path))

        # key is a dictionary, recursively handle
        elif type(content_dict[key]) == dict:
            refs.extend(_rec_scan_dict(content_dict[key], parent_path + [key]))

        # key is a list, recursively handle
        elif type(content_dict[key]) == list:
            refs.extend(_rec_scan_list(content_dict[key], parent_path + [key]))

        # key is a value, leaf node
        else:
            print(f'STRAIGHT UP | {key}: {content_dict[key]}')

    return refs



def parse_yaml_refs(yaml_content: dict):
    """
    Parses a list of references made within the given YAML content
    """
    return _rec_scan_dict(yaml_content, [])


def validate_refs():
    # TODO impl
    pass


def make_replacements(yaml_content: dict, ref_list: list):
    """
    Replaces references in given YAML content with evaluated structures
    Returns new copy of final merged YAML content
    """
    # create deep copy to make modifications to
    merged = deepcopy(yaml_content)

    for ref in ref_list:
        print(ref)
        pass


    return merged



def _main():

    content = _read_yaml('./tests/mergable.yaml')
    # content = _read_yaml('./tests/simple.yaml')

    refs = parse_yaml_refs(content)

    print(f'REF LIST: {refs}')

    if not refs:
        print('YAML contains no references\n')
        return 0

    merged = make_replacements(content, refs)



if __name__ == '__main__':
    _main()
