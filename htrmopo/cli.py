#
# Copyright 2025 Benjamin Kiessling
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
htrmopo.cli
~~~~~~~~~~~

Command line driver for interacting with the model repository.
"""
import os
import logging

import click

from rich import print
from rich.tree import Tree
from rich.table import Table
from rich.console import group, Group
from rich.traceback import install
from rich.logging import RichHandler
from rich.markdown import Markdown
from rich.progress import Progress

from collections import defaultdict

from htrmopo.util import make_printable, is_printable, iso15924_to_name, iso639_3_to_name

logging.captureWarnings(True)
logger = logging.getLogger('htrmopo')


# install rich traceback handler
install(suppress=[click])


def message(msg: str, **styles) -> None:
    if logger.getEffectiveLevel() >= 30:
        click.secho(msg, **styles)


def _render_creators(creators):
    o = []
    for creator in creators:
        c_text = creator['name']
        if (orcid := creator.get('orcid', None)) is not None:
            c_text += f' ({orcid})'
        if (affiliation:= creator.get('affiliation', None)) is not None:
            c_text += f' ({affiliation})'
        o.append(c_text)
    return o


def _render_metrics(metrics):
    return [f'{k}: {v:.2f}' for k, v in metrics.items()]


@click.group(chain=False)
@click.version_option()
@click.option('-v', '--verbose', default=0, count=True, show_default=True)
def cli(verbose):
    """
    Base command for repository interaction.
    """
    ctx = click.get_current_context()
    ctx.meta['verbose'] = verbose

    logger.addHandler(RichHandler(rich_tracebacks=True))
    logger.setLevel(level=30 - min(10 * verbose, 20))


@cli.command('show')
@click.pass_context
@click.option('-V', '--metadata-version',
              default='highest',
              type=click.Choice(['v0', 'v1', 'highest']),
              help='Version of metadata to fetch if multiple exist in repository.')
@click.argument('model_id')
def show(ctx, metadata_version, model_id):
    """
    Retrieves a model description from the repository.
    """
    from htrmopo import get_description

    if metadata_version == 'highest':
        metadata_version = None

    try:
        desc = get_description(model_id, version=metadata_version)
    except ValueError as e:
        logger.error(e)
        ctx.exit(1)

    if desc.version == 'v0':
        chars = []
        combining = []
        for char in sorted(desc.graphemes):
            if not is_printable(char):
                combining.append(make_printable(char))
            else:
                chars.append(char)

        table = Table(title=desc.summary, show_header=False)
        table.add_column('key', justify="left", no_wrap=True)
        table.add_column('value', justify="left", no_wrap=False)
        table.add_row('DOI', desc.doi)
        table.add_row('concept DOI', desc.concept_doi)
        table.add_row('publication date', desc.publication_date.isoformat())
        table.add_row('model type', Group(*desc.model_type))
        table.add_row('script', Group(*[iso15924_to_name(x) for x in desc.script]))
        table.add_row('alphabet', Group(' '.join(chars), ', '.join(combining)))
        table.add_row('keywords', Group(*desc.keywords))
        table.add_row('metrics', Group(*_render_metrics(desc.metrics)))
        table.add_row('license', desc.license)
        table.add_row('creators', Group(*_render_creators(desc.creators)))
        table.add_row('description', desc.description)
    elif desc.version == 'v1':
        table = Table(title=desc.summary, show_header=False)
        table.add_column('key', justify="left", no_wrap=True)
        table.add_column('value', justify="left", no_wrap=False)
        table.add_row('DOI', desc.doi)
        table.add_row('concept DOI', desc.concept_doi)
        table.add_row('publication date', desc.publication_date.isoformat())
        table.add_row('model type', Group(*desc.model_type))
        table.add_row('language', Group(*[iso639_3_to_name(x) for x in desc.language]))
        table.add_row('script', Group(*[iso15924_to_name(x) for x in desc.script]))
        table.add_row('keywords', Group(*desc.keywords))
        table.add_row('datasets', Group(*desc.datasets))
        table.add_row('metrics', Group(*_render_metrics(desc.metrics)))
        table.add_row('base model', Group(*desc.base_model))
        table.add_row('software', desc.software_name)
        table.add_row('software_hints', Group(*desc.software_hints))
        table.add_row('license', desc.license)
        table.add_row('creators', Group(*_render_creators(desc.creators)))
        table.add_row('description', Markdown(desc.description))

    print(table)


@cli.command('list')
@click.pass_context
@click.option('-F', '--from-date',
              default=None,
              type=click.STRING,
              help='ISO-8601 date string to filter repository entries by age.')
def list_models(ctx, from_date):
    """
    Lists models in the repository.
    """
    from htrmopo import get_listing

    with Progress() as progress:
        download_task = progress.add_task('Retrieving model list', total=0, visible=True)
        repository = get_listing(lambda total, advance: progress.update(download_task, total=total, advance=advance), from_date=from_date)
    # aggregate models under their concept DOI
    concepts = defaultdict(list)
    for item in repository.values():
        # both got the same DOI information
        record = item['v0'] if item['v0'] else item['v1']
        concepts[record.concept_doi].append(record.doi)

    table = Table(show_header=True)
    table.add_column('DOI', justify="left", no_wrap=True)
    table.add_column('summary', justify="left", no_wrap=False)
    table.add_column('model type', justify="left", no_wrap=False)
    table.add_column('keywords', justify="left", no_wrap=False)

    for k, v in concepts.items():
        records = [repository[x]['v1'] if 'v1' in repository[x] else repository[x]['v0'] for x in v]
        records = sorted(records, key=lambda x: x.publication_date, reverse=True)
        tree_node = k if len(records) > 1 else v[0]
        t = Tree(tree_node)
        if len(records) > 1:
            [t.add(x.doi) for x in records]
            prefix = ['']
        else:
            prefix = []
        table.add_row(t,
                      Group(*prefix + [x.summary for x in records]),
                      Group(*prefix + ['; '.join(x.model_type) for x in records]),
                      Group(*prefix + ['; '.join(x.keywords) for x in records]))

    print(table)
    ctx.exit(0)


@cli.command('get')
@click.pass_context
@click.argument('model_id')
def get(ctx, model_id):
    """
    Retrieves a model from the repository.
    """
    from kraken import repo
    from kraken.lib.progress import KrakenDownloadProgressBar

    try:
        os.makedirs(click.get_app_dir(APP_NAME))
    except OSError:
        pass

    with KrakenDownloadProgressBar() as progress:
        download_task = progress.add_task('Processing', total=0, visible=True if not ctx.meta['verbose'] else False)
        filename = repo.get_model(model_id, click.get_app_dir(APP_NAME),
                                  lambda total, advance: progress.update(download_task, total=total, advance=advance))
    message(f'Model name: {filename}')
    ctx.exit(0)


@click.command('publish')
@click.pass_context
@click.option('-i', '--metadata', show_default=True,
              type=click.File(mode='r', lazy=True), help='Model card file for the model.')
@click.option('-a', '--access-token', prompt=True, help='Zenodo access token')
@click.option('-p', '--private/--public', default=False, help='Disables Zenodo '
              'community inclusion request. Allows upload of models that will not show '
              'up on `htrmopo list` output')
@click.argument('model', nargs=1, type=click.Path(exists=False, readable=True, dir_okay=True))
def publish(ctx, metadata, access_token, private, model):
    """
    Publishes a model on the Zenodo model repository.
    """
    import json

    import importlib_resources
    from jsonschema import validate
    from jsonschema.exceptions import ValidationError

    from kraken import repo
    from kraken.lib import models
    from kraken.lib.progress import KrakenDownloadProgressBar

    ref = importlib_resources.files('kraken').joinpath('metadata.schema.json')
    with open(ref, 'rb') as fp:
        schema = json.load(fp)

    nn = models.load_any(model)

    if not metadata:
        author = click.prompt('author')
        affiliation = click.prompt('affiliation')
        summary = click.prompt('summary')
        description = click.edit('Write long form description (training data, transcription standards) of the model here')
        accuracy_default = None
        # take last accuracy measurement in model metadata
        if 'accuracy' in nn.nn.user_metadata and nn.nn.user_metadata['accuracy']:
            accuracy_default = nn.nn.user_metadata['accuracy'][-1][1] * 100
        accuracy = click.prompt('accuracy on test set', type=float, default=accuracy_default)
        script = [
            click.prompt(
                'script',
                type=click.Choice(
                    sorted(
                        schema['properties']['script']['items']['enum'])),
                show_choices=True)]
        license = click.prompt(
            'license',
            type=click.Choice(
                sorted(
                    schema['properties']['license']['enum'])),
            show_choices=True)
        metadata = {
            'authors': [{'name': author, 'affiliation': affiliation}],
            'summary': summary,
            'description': description,
            'accuracy': accuracy,
            'license': license,
            'script': script,
            'name': os.path.basename(model),
            'graphemes': ['a']
        }
        while True:
            try:
                validate(metadata, schema)
            except ValidationError as e:
                message(e.message)
                metadata[e.path[-1]] = click.prompt(e.path[-1], type=float if e.schema['type'] == 'number' else str)
                continue
            break

    else:
        metadata = json.load(metadata)
        validate(metadata, schema)
    metadata['graphemes'] = [char for char in ''.join(nn.codec.c2l.keys())]
    with KrakenDownloadProgressBar() as progress:
        upload_task = progress.add_task('Uploading', total=0, visible=True if not ctx.meta['verbose'] else False)
        oid = repo.publish_model(model, metadata, access_token, lambda total, advance: progress.update(upload_task, total=total, advance=advance), private)
    message('model PID: {}'.format(oid))