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
DCAT record class for Sickle
"""
from sickle.models import Header, Record

from dataclasses import dataclass, field
from typing import TypedDict, Optional, Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    import datetime.datetime


def dcat_to_dict(tree):
    """Converts a DCAT XML tree to a dictionary.
    """
    title = t.text if (t := tree.find('./{*}RDF/{*}Description/{*}title')) is not None else None

    distribution = []
    for element in tree.findall('./{*}RDF/{*}Description/{*}distribution'):
        if (file_url := element.find('./{*}Distribution/{*}downloadURL')) is not None:
            distribution.append({'url': file_url.attrib.values()[0],
                                 'size': int(siz.text) if (siz := element.find('./{*}Distribution/{*}byteSize')) is not None else -1})
    if (description := tree.find('./{*}RDF/{*}Description/{*}description')) is not None:
        description = description.text
    keywords = [keyword.text for keyword in tree.findall('./{*}RDF/{*}Description/{*}keyword')]
    creators = []
    for creator in tree.findall('./{*}RDF/{*}Description/{*}creator/{*}Description'):
        creators.append({'name': c.text if (c := creator.find('./{*}name')) is not None else '',
                         'orcid': o[0] if len(o := [v for k, v in creator.attrib.items() if k.endswith('about')]) else None,
                         'affiliation': a.text if (a := creator.find('./{*}memberOf//{*}name')) is not None else ''})
    if (concept := tree.find('./{*}RDF/{*}Description/{*}isVersionOf/{*}Description/{*}identifier')) is not None:
        concept = concept.text
    return {'doi': d.text if (d := tree.find('./{*}RDF/{*}Description/{*}identifier')) is not None else None,
            'summary': title,
            'description': description,
            'distribution': distribution,
            'creators': creators,
            'keywords': keywords,
            'concept_doi': concept
            }


class DCATRecord(Record):
    """Represents an OAI DCAT record.

    :param record_element: The XML element 'record'.
    :type record_element: :class:`lxml.etree._Element`
    :param strip_ns: Flag for whether to remove the namespaces from the
                     element names.
    """

    def __init__(self, record_element, strip_ns=True):
        super(Record, self).__init__(record_element, strip_ns=strip_ns)
        self.header = Header(self.xml.find(
            './/' + self._oai_namespace + 'header'))
        self.deleted = self.header.deleted
        if not self.deleted:
            self.metadata = self.get_metadata()

    def __repr__(self):
        if self.header.deleted:
            return '<Record %s [deleted]>' % self.header.identifier
        else:
            return '<Record %s>' % self.header.identifier

    def __iter__(self):
        return iter(self.metadata.items())

    def get_metadata(self):
        return dcat_to_dict(self.xml.find('.//{*}metadata'))


class AuthorDict(TypedDict):
    author: str
    affiliation: Optional[str]
    orcid: Optional[str]


class DistributionDict(TypedDict):
    url: str
    size: int


class v0MetricsDict(TypedDict):
    cer: float


@dataclass
class v1RepositoryRecord:
    """
    A v1 record in the repository representing a single ATR model.
    """
    doi: str
    concept_doi: str
    creators: List[AuthorDict]
    summary: str
    description: str
    license: str
    software_name: str
    script: List[str]
    language: List[str]
    publication_date: 'datetime.datetime'
    distribution: List[DistributionDict]
    model_type: List[str]
    license_url: Optional[str] = None
    software_hints: Optional[List[str]] = None
    model_type: Optional[List[str]] = None
    metrics: Optional[Dict[str, float]] = None
    datasets: Optional[List[str]] = None
    base_model: Optional[List[str]] = None
    keywords: Optional[List[str]] = None
    citation: Optional[str] = None
    version: str = 'v1'


@dataclass
class v0RepositoryRecord:
    """
    A v0 record in the repository representing a single ATR model.
    """
    doi: str
    concept_doi: str
    creators: List[AuthorDict]
    summary: str
    description: str
    metrics: v0MetricsDict
    license: str
    script: List[str]
    distribution: List[DistributionDict]
    graphemes: List[str]
    publication_date: 'datetime.datetime'
    model_type: List[str] = field(default_factory=lambda: ['recognition'])
    keywords: Optional[List[str]] = None
    version: str = 'v0'
