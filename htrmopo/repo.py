#
# Copyright 2024 Benjamin Kiessling
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing
# permissions and limitations under the License.
"""
Accessors to the v2 model repository on zenodo.
"""
import yaml
import uuid
import logging
import requests

from collections import defaultdict
from contextlib import closing
from pathlib import Path
from sickle import Sickle
from urllib.parse import urlsplit
from platformdirs import user_data_dir
from jsonschema import validate
from dateutil.parser import parse as date_parse

from typing import TYPE_CHECKING, Any, Callable, Optional, Literal, Union, Dict


from htrmopo.record import DCATRecord, v0RepositoryRecord, v1RepositoryRecord
from htrmopo.util import (_yaml_regex, _v1_schema, _v0_schema, _doi_to_oai_id,
                          _doi_to_zenodo_id, get_repo_url, get_oai_url,
                          format_checker)

if TYPE_CHECKING:
    from os import PathLike

__all__ = ['get_model', 'get_description', 'get_listing']

logger = logging.getLogger(__name__)

sickle = Sickle(get_oai_url())
sickle.class_mapping['ListRecords'] = DCATRecord
sickle.class_mapping['GetRecord'] = DCATRecord


def _build_v0_record(metadata, request):
    try:
        json_metadata = request.json()
    except Exception:
        raise Exception(f'Metadata for {metadata["doi"]} not in JSON format')
    validate(json_metadata, _v0_schema, format_checker=format_checker)
    metadata.update(json_metadata)
    metadata['creators'].extend(metadata['authors'])
    metadata['doi'] = urlsplit(metadata['doi']).path[1:]
    metadata['concept_doi'] = urlsplit(metadata['concept_doi']).path[1:]
    metadata['metrics'] = {'cer': (100 - float(metadata.pop('accuracy')))}
    metadata.pop('authors')
    metadata.pop('name')
    return v0RepositoryRecord(**metadata)


def _build_v1_record(metadata, model_card):
    header, content = _yaml_regex.match(model_card).groups()
    try:
        yaml_metadata = yaml.safe_load(header)
    except Exception:
        raise Exception(f'Metadata for {metadata["doi"]} not in YAML format')
    validate(yaml_metadata, _v1_schema, format_checker=format_checker)
    metadata.update(yaml_metadata)
    if metadata['license'].startswith('other'):
        metadata['license'] = metadata['license_name']
        metadata.pop('license_name')
    # merge authors and creators
    metadata['creators'].extend(metadata['authors'])
    metadata['doi'] = urlsplit(metadata['doi']).path[1:]
    metadata['concept_doi'] = urlsplit(metadata['concept_doi']).path[1:]
    metadata.pop('id')
    metadata.pop('authors')
    metadata.pop('description', None)
    metadata['keywords'] = list({*metadata.pop('keywords', None), *metadata.pop('tags', None)})
    return v1RepositoryRecord(description=content, **metadata)


def get_model(model_id: str,
              path: Optional[Union[str, 'PathLike']] = None,
              callback: Callable[[int, int], Any] = lambda total, advance: None,
              abort_if_exists: bool = False) -> 'PathLike':
    """
    Retrieves a model and their files to a path.

    Args:
        model_id: DOI of the model
        path: Optional destination path to write model to. If none is given a
              new one will be created in the htrmopo data dir.
        callback: Function called for every 1024 octet chunk received.
        version: Which version of the metadata should be returned if more than
                 one exists. Per default the newest is returned.

    Returns:
        The output path under which the model files have been placed.
    """
    logger.info(f'Saving model {model_id} to {path}')
    if (oai_id := _doi_to_oai_id(model_id)) is None:
        raise ValueError(f'{model_id} is not a valid DOI')
    try:
        record = sickle.GetRecord(identifier=oai_id, metadataPrefix='dcat')
    except requests.HTTPError:
        # might just be a concept DOI which don't show up in OAI. Try to
        # resolve it through the search API.
        r = requests.get(f'{get_repo_url()}records/{_doi_to_zenodo_id(model_id)}')
        r.raise_for_status()
        model_id = r.json()['doi']
        real_oai_id = _doi_to_oai_id(model_id)
        record = sickle.GetRecord(identifier=real_oai_id, metadataPrefix='dcat')

    if path is not None:
        path = Path(path).resolve()
    else:
        path = Path(user_data_dir('htrmopo')) / str(uuid.uuid5(uuid.NAMESPACE_DNS, model_id))

    if path.exists():
        if abort_if_exists:
            raise ValueError(f'Output path {path} already exists.')
        else:
            logger.warning(f'Output path {path} already exists.')

    path.mkdir(parents=True, exist_ok=True)

    callback(0, 0)
    metadata = record.metadata
    model_size = sum([file['size'] for file in metadata['distribution']])
    for file in metadata['distribution']:
        name = Path(urlsplit(file['url']).path).name
        output_path = (path / name).resolve()
        if not output_path.is_relative_to(path):
            logger.warning(f'Found file {name} with invalid path.')
            continue
        logger.info(f'Downloading model file {file["url"]} to {output_path}')
        with closing(requests.get(file["url"], stream=True)) as r:
            with open(output_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    callback(model_size, len(chunk))
                    f.write(chunk)
    return path


def get_description(model_id: str,
                    callback: Callable[..., Any] = lambda: None,
                    version: Optional[Literal['v0', 'v1']] = None) -> Union[v0RepositoryRecord, v1RepositoryRecord]:
    """
    Fetches the metadata for a single model from the zenodo repository.

    Args:
        model_id: DOI of the model.
        callback: Optional function called once per HTTP request.
        version: Which version of the metadata should be returned if more than
                 one exists. Per default the newest is returned.

    Returns:
        Dict
    """
    logger.info(f'Retrieving metadata for {model_id}')
    if (oai_id := _doi_to_oai_id(model_id)) is None:
        raise ValueError(f'{model_id} is not a valid DOI')
    try:
        record = sickle.GetRecord(identifier=oai_id, metadataPrefix='dcat')
    except requests.HTTPError:
        # might just be a concept DOI which don't show up in OAI. Try to
        # resolve it through the search API.
        r = requests.get(f'{get_repo_url()}records/{_doi_to_zenodo_id(model_id)}')
        r.raise_for_status()
        real_oai_id = _doi_to_oai_id(r.json()['doi'])
        record = sickle.GetRecord(identifier=real_oai_id, metadataPrefix='dcat')

    callback()
    repo_record = None
    for file in record.metadata['distribution']:
        # Zenodo deposits do not contain directories so we can just check for
        # file name.
        name = Path(urlsplit(file['url']).path).name
        if name == 'README.md':  # v1 model
            if version == 'v0':
                continue
            callback()
            r = requests.get(file['url'])
            r.raise_for_status()
            metadata = record.metadata.copy()
            metadata['publication_date'] = date_parse(record.header.datestamp)
            try:
                repo_record = _build_v1_record(metadata, r.content.decode('utf-8'))
            except Exception as e:
                logger.info(f'Invalid metadata for {model_id}: {e}')
        if name == 'metadata.json':  # v0 model
            if version != 'v0' and repo_record:
                break
            callback()
            r = requests.get(file['url'])
            r.raise_for_status()
            metadata = record.metadata.copy()
            metadata['publication_date'] = date_parse(record.header.datestamp)
            try:
                repo_record = _build_v0_record(metadata, r)
            except Exception as e:
                logger.info(f'Invalid metadata for {model_id}: {e}')

    if not repo_record:
        raise ValueError(f"No metadata found for \'{model_id}\'")
    return repo_record


def get_listing(callback: Callable[[int, int], Any] = lambda total, advance: None,
                from_date: Optional[str] = None) -> Dict[str, Dict[str, Union[v0RepositoryRecord, v1RepositoryRecord]]]:
    """
    Fetches a listing of all models from the zenodo repository.

    Args:
        callback: Function called for each processed record.
        from_date: Lower limit of time stamp to harvest.

    Returns:
        Dict of models with each model.
    """
    items = defaultdict(dict)
    # get all identiifers first just to get total number of items in repository
    total = len(list(sickle.ListIdentifiers(metadataPrefix='dcat', set='user-ocr_models', **{'from': from_date})))
    callback(total, 0)
    for record in sickle.ListRecords(metadataPrefix='dcat', set='user-ocr_models', **{'from': from_date}):
        doi = urlsplit(record.metadata['doi']).path[1:]
        for file_url in record.metadata['distribution']:
            if file_url['url'].endswith('README.md'):  # v1 model
                r = requests.get(file_url['url'])
                r.raise_for_status()
                metadata = record.metadata.copy()
                metadata['publication_date'] = date_parse(record.header.datestamp)
                try:
                    items[doi]['v1'] = _build_v1_record(metadata, r.content.decode('utf-8'))
                except Exception as e:
                    logger.info(f'Invalid metadata for {doi}: {e}')
            if file_url['url'].endswith('metadata.json'):  # v0 model
                r = requests.get(file_url['url'])
                r.raise_for_status()
                metadata = record.metadata.copy()
                metadata['publication_date'] = date_parse(record.header.datestamp)
                try:
                    items[doi]['v0'] = _build_v0_record(metadata, r)
                except Exception as e:
                    logger.info(f'Invalid metadata for {doi}: {e}')
        callback(total, 1)
    return dict(items)
