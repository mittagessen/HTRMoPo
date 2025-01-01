import re
import json
import unicodedata
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

with open(importlib_resources.files('htrmopo').joinpath('iso15924.txt')) as fp:
    _iso15924 = {}
    for line in fp.readlines():
        try:
            code, _, name, *_ =  line.split(';')
            _iso15924[code] = name
        except Exception:
            continue

with open(importlib_resources.files('htrmopo').joinpath('iso639-3.txt')) as fp:
    _iso639_3 = {}
    for line in fp.readlines()[1:]:
        try:
            code , name, *_ =  line.split('\t')
            _iso639_3[code] = name
        except Exception:
            continue


def iso639_3_to_name(script):
    return _iso639_3[script]


def iso15924_to_name(script):
    return _iso15924[script]


def _doi_to_oai_id(doi: str) -> str:
    """
    Constructs a zenodo OAI identifier from a DOI.

    Args:
        doi: Zenodo DOI
    """
    identifier = re.match(r'[0-9.]+\/zenodo\.([0-9]+)', doi)
    if identifier is not None:
        identifier = identifier.groups()[0]
        return f'oai:zenodo.org:{identifier}'


def _doi_to_zenodo_id(doi: str) -> str:
    """
    Extracts a zenodo record ID from a DOI.

    Args:
        doi: Zenodo DOI
    """
    identifier = re.match(r'[0-9.]+\/zenodo\.([0-9]+)', doi)
    if identifier is not None:
        identifier = identifier.groups()[0]
        return identifier


def is_printable(char: str) -> bool:
    """
    Determines if a chode point is printable/visible when printed.

    Args:
        char: Input code point.

    Returns:
        True if printable, False otherwise.
    """
    letters = ('LC', 'Ll', 'Lm', 'Lo', 'Lt', 'Lu')
    numbers = ('Nd', 'Nl', 'No')
    punctuation = ('Pc', 'Pd', 'Pe', 'Pf', 'Pi', 'Po', 'Ps')
    symbol = ('Sc', 'Sk', 'Sm', 'So')
    printable = letters + numbers + punctuation + symbol

    return unicodedata.category(char) in printable


def make_printable(char: str) -> str:
    """
    Takes a Unicode code point and return a printable representation of it.

    Args:
        char: Input code point

    Returns:
        Either the original code point, the name of the code point if it is a
        combining mark, whitespace etc., or the hex code if it is a control
        symbol.
    """
    if not char or is_printable(char):
        return char
    elif unicodedata.category(char) in ('Cc', 'Cs', 'Co'):
        return '0x{:x}'.format(ord(char))
    else:
        return unicodedata.name(char)

