#!/usr/bin/env python3

import yaml



# YAML REFERENCE STRUCTURE
# $replace<#sub-field?>: <path-to-file?>#<path-to-object>


def read_yaml(file_path: str):
    """
    Read in given YAML file
    """
    try:
        with open(file_path, 'r') as file:
            yaml_content = yaml.safe_load(file)
            return yaml_content
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'")
    except yaml.YAMLError as e:
        print(f"Error: Could not parse YAML file. {e}")
    return None


def main():
    print(read_yaml('./tests/test.yaml'))


if __name__ == '__main__':
    main()
