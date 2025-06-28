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


def _rec_scan_list(content_list: list):
    """
    Scans the given list recursively for references
    Returns: list of detected references in the YAMl file
    """
    for item in content_list:
        # nested list, recursively handle
        if type(item) == list:
            _rec_scan_list(item)

        # nested dictionary, recursively handle
        elif type(item) == dict:
            _rec_scan_dict(item)

        # value, leaf node
        else:
            print(f'PLEB ITEM: {item}')


def _rec_scan_dict(content_dict: dict):
    """
    Scans the given YAML dictionary recursively for references
    Returns: list of detected references in the YAML file
    """
    # iterate over keys at the top-level of the given YAML
    for key in content_dict.keys():
        # check if key is a reference
        if key.startswith(constants.REFERENCE_KEY):
            # TODO validate path string? Or separate function
            print(content_dict[key])

        # key is a dictionary, recursively handle
        elif type(content_dict[key]) == dict:
            _rec_scan_dict(content_dict[key])

        # key is a list, recursively handle
        elif type(content_dict[key]) == list:
            _rec_scan_list(content_dict[key])

        # key is a value, leaf node
        else:
            print(f'STRAIGHT UP | {key}: {content_dict[key]}')



def parse_yaml_refs(yaml_content: dict):
    """
    Parses a list of references made within the given YAML content
    """
    _rec_scan_dict(yaml_content)




def _main():
    # content = read_yaml('./tests/mergable.yaml')
    content = _read_yaml('./tests/simple.yaml')

    refs = parse_yaml_refs(content)

    print(f'LIST: {refs}')

    # make_replacements(content, refs)



if __name__ == '__main__':
    _main()
