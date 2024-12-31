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
import os
import yaml
import json
import logging
import requests

from typing import TYPE_CHECKING, Any, Callable
from pathlib import Path
from markdown import markdown
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from htrmopo.util import _yaml_regex, _v1_schema, _doi_to_zenodo_id

if TYPE_CHECKING:
    from os import PathLike

__all__ = ['update_model', 'publish_model']

logger = logging.getLogger(__name__)

MODEL_REPO = 'https://zenodo.org/api/'


def update_model(model_id: str,
                 model: 'PathLike',
                 model_card: str,
                 access_token: str,
                 callback: Callable[[int, int], Any] = lambda total, advance: None,
                 private: bool = False) -> str:
    """
    Updates a model in the repository by creating a new version of an existing
    record.

    Args:
        model_id: Model (NOT concept ID) of the record to create a new version
                  for.
        model: Path to read model from. Can be a single file or a directory.
        model_card: String of a Markdown document with YAML front matter
                    containing the model card + associated metadata.
        access_token: Zenodo API access token
        callback: Function called with octet-wise progress.
        private: Whether to generate a community inclusion request that makes
                 the model recoverable by the public.
    """
    model = Path(model)
    if not model.exists():
        raise ValueError('Model path {model} does not exist.')
    # find all files for the deposition
    model_size = len(model_card.encode('utf-8'))
    if model.is_dir():
        model_files = []
        for file in model.iterdir():
            if file.relative_to(model) == Path('README.md'):
                logger.warning('Found a README.md in root of model dir. Ignoring.')
                continue
            if file.is_dir():
                logger.warning(f'Zenodo depositions are flat. Found dir {file}. Skipping')
                continue
            model_files.append(file)
            model_size += file.stat().st_size
    else:
        model_files = [model]
        model_size += model.stat().st_size

    logger.info(f'Got {len(model_files)} files for model with size of {model_size} bytes.')
    # validate model card
    header, content = _yaml_regex.match(model_card).groups()
    mopo_metadata = yaml.safe_load(header)
    validate(mopo_metadata, _v1_schema)

    # create a new draft version of an existing deposition.
    recid = _doi_to_zenodo_id(model_id)
    r = requests.post(f'{MODEL_REPO}records/{recid}/versions', params={'access_token': access_token})
    r.raise_for_status()
    callback(model_size, 1)
    new_recid = r.json()['id']
    r = requests.get(f'{MODEL_REPO}deposit/depositions/{new_recid}', params={'access_token': access_token})
    r.raise_for_status()
    callback(model_size, 1)
    depo = r.json()
    bucket_url = depo['links']['bucket']

    # finalize metadata record
    mopo_metadata['id'] = depo['metadata']['prereserve_doi']['doi']
    header = yaml.dump(mopo_metadata)
    _metadata = f'---\n{header}---\n{content}'.encode('utf-8')

    # push metadata file
    r = requests.put(f'{bucket_url}/README.md',
                     params={'access_token': access_token},
                     data=_metadata)
    r.raise_for_status()
    callback(model_size, len(_metadata))
    # push all other files
    for file in model_files:
        with open(file, 'rb') as fp:
            r = requests.put(f'{bucket_url}/{file.name}',
                             params={'access_token': access_token},
                             data=fp)
            r.raise_for_status()
            callback(model_size, file.stat().st_size)

    # fill zenodo metadata
    data = {'metadata': {
                        'title': mopo_metadata['summary'],
                        'upload_type': 'publication',
                        'publication_type': 'other',
                        'description': markdown(content),
                        'creators': mopo_metadata['authors'],
                        'access_right': 'open',
                        'license': mopo_metadata['license']
                        }
            }

    # add keywords
    if 'tags' in mopo_metadata and mopo_metadata['tags']:
        data['metadata']['keywords'] = mopo_metadata['tags']

    if not private:
        data['metadata']['communities'] = [{'identifier': 'ocr_models'}]

    # add link to training data to metadata
    if 'datasets' in mopo_metadata and mopo_metadata['datasets']:
        data['metadata']['related_identifiers'] = [{'relation': 'isDerivedFrom', 'identifier': ds, 'resource_type': 'dataset'} for ds in mopo_metadata['datasets']]

    if 'base_model' in mopo_metadata and mopo_metadata['base_model']:
        if 'related_identifiers' not in data['metadata']:
            data['metadata']['related_identifiers'] = []
        data['metadata']['related_identifiers'].extend([{'relation': 'isDerivedFrom', 'identifier': mid, 'resource_type': 'other'} for mid in mopo_metadata['base_model']])

    r = requests.put(f'{MODEL_REPO}deposit/depositions/{new_recid}',
                     params={'access_token': access_token},
                     data=json.dumps(data),
                     headers={"Content-Type": "application/json"})

    r.raise_for_status()
    callback(model_size, 1)
    r = requests.post(f'{MODEL_REPO}deposit/depositions/{new_recid}/actions/publish',
                      params={'access_token': access_token})
    r.raise_for_status()
    callback(model_size, 1)
    return r.json()['doi']


def publish_model(model: 'PathLike',
                  model_card: str,
                  access_token: str,
                  callback: Callable[[int, int], Any] = lambda total, advance: None,
                  private: bool = False) -> str:
    """
    Publishes a model to the repository.

    Args:
        model: Path to read model from. Can be a single file or a directory.
        model_card: String of a Markdown document with YAML front matter
                    containing the model card + associated metadata.
        access_token: Zenodo API access token
        callback: Function called with octet-wise progress.
        private: Whether to generate a community inclusion request that makes
                 the model recoverable by the public.
    """
    model = Path(model)
    if not model.exists():
        raise ValueError('Model path {model} does not exist.')
    # find all files for the deposition
    model_size = len(model_card.encode('utf-8'))
    if model.is_dir():
        model_files = []
        for file in model.iterdir():
            if file.relative_to(model) == Path('README.md'):
                logger.warning('Found a README.md in root of model dir. Ignoring.')
                continue
            if file.is_dir():
                logger.warning(f'Zenodo depositions are flat. Found dir {file}. Skipping')
                continue
            model_files.append(file)
            model_size += file.stat().st_size
    else:
        model_files = [model]
        model_size += model.stat().st_size

    logger.info(f'Got {len(model_files)} files for model with size of {model_size} bytes.')
    # validate model card
    header, content = _yaml_regex.match(model_card).groups()
    mopo_metadata = yaml.safe_load(header)
    validate(mopo_metadata, _v1_schema)

    # create new deposition
    headers = {"Content-Type": "application/json"}
    r = requests.post(f'{MODEL_REPO}deposit/depositions',
                      params={'access_token': access_token},
                      json={},
                      headers=headers)
    r.raise_for_status()
    callback(model_size, 1)
    depo = r.json()
    deposition_id = depo['id']
    bucket_url = depo['links']['bucket']

    # finalize metadata record
    mopo_metadata['id'] = depo['metadata']['prereserve_doi']['doi']
    header = yaml.dump(mopo_metadata)
    _metadata = f'---\n{header}---\n{content}'.encode('utf-8')

    # push metadata file
    r = requests.put(f'{bucket_url}/README.md',
                     params={'access_token': access_token},
                     data=_metadata)
    r.raise_for_status()
    callback(model_size, len(_metadata))
    # push all other files
    for file in model_files:
        with open(file, 'rb') as fp:
            r = requests.put(f'{bucket_url}/{file.name}',
                             params={'access_token': access_token},
                             data=fp)
            r.raise_for_status()
            callback(model_size, file.stat().st_size)

    # fill zenodo metadata
    data = {'metadata': {
                        'title': mopo_metadata['summary'],
                        'upload_type': 'publication',
                        'publication_type': 'other',
                        'description': markdown(content),
                        'creators': mopo_metadata['authors'],
                        'access_right': 'open',
                        'license': mopo_metadata['license']
                        }
            }

    # add keywords
    if 'tags' in mopo_metadata and mopo_metadata['tags']:
        data['metadata']['keywords'] = mopo_metadata['tags']

    if not private:
        data['metadata']['communities'] = [{'identifier': 'ocr_models'}]

    # add link to training data to metadata
    if 'datasets' in mopo_metadata and mopo_metadata['datasets']:
        data['metadata']['related_identifiers'] = [{'relation': 'isDerivedFrom', 'identifier': ds, 'resource_type': 'dataset'} for ds in mopo_metadata['datasets']]

    if 'base_model' in mopo_metadata and mopo_metadata['base_model']:
        if 'related_identifiers' not in data['metadata']:
            data['metadata']['related_identifiers'] = []
        data['metadata']['related_identifiers'].extend([{'relation': 'isDerivedFrom', 'identifier': mid, 'resource_type': 'other'} for mid in mopo_metadata['base_model']])

    r = requests.put(f'{MODEL_REPO}deposit/depositions/{deposition_id}',
                     params={'access_token': access_token},
                     data=json.dumps(data),
                     headers=headers)
    r.raise_for_status()
    callback(model_size, 1)
    r = requests.post(f'{MODEL_REPO}deposit/depositions/{deposition_id}/actions/publish',
                      params={'access_token': access_token})
    r.raise_for_status()
    callback(model_size, 1)
    return r.json()['doi']
