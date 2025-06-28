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
import os

# local module imports
from get_nested import get_nested
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
            # else:
            #     print(f'PLEB LIST ITEM: {item}')
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

        # # key is a value, leaf node
        # else:
        #     print(f'STRAIGHT UP | {key}: {content_dict[key]}')

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
    Takes
     - yaml_content | YAML dictionary to make reference replacements within
     - ref_list     | List of reference information of the form: (<ref key>, <ref path>, <path to ref>)
    Returns new copy of final merged YAML content
    """
    # create deep copy to make modifications to
    merged = deepcopy(yaml_content)

    for key, value, loc in ref_list:
        # TODO parse replacement key
        # TODO parse file path
        # parse replacement value
        # attempt to resolve value
        try:
            replacement_val = get_nested(yaml_content, value, '/')
        except LookupError as e:
            print('\nUNABLE TO MAKE REFERENCE SUBSTITUTION')
            print(f' {key}: {value} DID NOT SUCCESSFULLY RESOLVE')
            print(f' RESOLVE ERROR: {e}\n')
            # TODO evaluate if early exit is appropriate, or if ref should just be left unresolved

        # substitute ref for retreived value
        ref = merged
        for entry in loc[:-1]:
            ref = ref[entry]
        ref[loc[-1]] = replacement_val

    return merged



def _main():

    # TODO take commandline inputfile path
    content = _read_yaml('./tests/mergable.yaml')
    # content = _read_yaml('./tests/simple.yaml')

    refs = parse_yaml_refs(content)

    # print(f'REF LIST: {refs}')

    if not refs:
        print('YAML contains no references\n')
        return 0

    merged = make_replacements(content, refs)

    print()
    print(merged)
    print()

    # TODO take commandline outfile path
    # determine project dir and write file to output directory
    project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    with open(os.path.join(project_dir, 'output/merged.yaml'), 'w') as f:
        yaml.dump(merged, f)



if __name__ == '__main__':
    _main()
