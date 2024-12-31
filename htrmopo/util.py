import re
import json
import importlib_resources

_yaml_delim = r'(?:---|\+\+\+)'
_yaml = r'(.*?)'
_content = r'\s*(.+)$'
_re_pattern = r'^\s*' + _yaml_delim + _yaml + _yaml_delim + _content
_yaml_regex = re.compile(_re_pattern, re.S | re.M)

with open(importlib_resources.files('htrmopo').joinpath('v1.metadata.schema.json')) as fp:
    _v1_schema = json.load(fp)

with open(importlib_resources.files('htrmopo').joinpath('v0.metadata.schema.json')) as fp:
    _v0_schema = json.load(fp)


def _doi_to_oai_id(doi: str) -> str:
    identifier = re.match(r'[0-9.]+\/zenodo\.([0-9]+)', doi)
    if identifier is not None:
        identifier = identifier.groups()[0]
        return f'oai:zenodo.org:{identifier}'


def _doi_to_zenodo_id(doi: str) -> str:
    identifier = re.match(r'[0-9.]+\/zenodo\.([0-9]+)', doi)
    if identifier is not None:
        identifier = identifier.groups()[0]
        return identifier


