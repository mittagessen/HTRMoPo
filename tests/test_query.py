# -*- coding: utf-8 -*-
import shutil
import tempfile
import unittest
from pathlib import Path

from htrmopo import get_listing, get_description, get_model
from htrmopo.record import v0RepositoryRecord, v1RepositoryRecord

thisfile = Path(__file__).resolve().parent
resources = thisfile / 'resources'


def _check_file_in_model_dir(dir_path, file_name, size):
    for file in dir_path.iterdir():
        if file.name == file_name and file.stat().st_size == size:
            return True
    return False


class TestQuery(unittest.TestCase):
    """
    Testing querying the model repository.
    """

    def setUp(self):
        self.temp_model = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_model.name)

    def tearDown(self):
        shutil.rmtree(self.temp_model.name)

    def test_listing(self):
        """
        Tests fetching the model list.
        """
        records = get_listing()
        self.assertGreater(len(records), 15)

    def test_get_description_v0(self):
        """
        Tests fetching the description of a v0 model.
        """
        record = get_description('10.5281/zenodo.8425684')
        self.assertIsInstance(record, v0RepositoryRecord)
        self.assertEqual(record.doi, '10.5281/zenodo.8425684')

    def test_get_description_concept_doi_v0(self):
        """
        Tests fetching the description of a v0 model by concept DOI.
        """
        record = get_description('10.5281/zenodo.8425683')
        self.assertIsInstance(record, v0RepositoryRecord)
        self.assertEqual(record.concept_doi, '10.5281/zenodo.8425683')
        self.assertNotEqual(record.doi, '10.5281/zenodo.8425683')

    def test_get_description_prev_version_v0(self):
        """
        Tests fetching the description of a v0 model that has a superseding newer version.
        """
        record = get_description('10.5281/zenodo.6657809')
        self.assertIsInstance(record, v0RepositoryRecord)
        self.assertEqual(record.doi, '10.5281/zenodo.6657809')
        self.assertEqual(record.concept_doi, '10.5281/zenodo.6657808')

    def test_get_description_v1(self):
        """
        Tests fetching the description of a v1 model.
        """
        record = get_description('10.5281/zenodo.14585602')
        self.assertIsInstance(record, v1RepositoryRecord)
        self.assertEqual(record.doi, '10.5281/zenodo.14585602')

    def test_get_description_concept_doi_v1(self):
        """
        Tests fetching the description of a v1 model by concept DOI.
        """
        record = get_description('10.5281/zenodo.7051645')
        self.assertIsInstance(record, v1RepositoryRecord)
        self.assertEqual(record.concept_doi, '10.5281/zenodo.7051645')
        self.assertNotEqual(record.doi, '10.5281/zenodo.7051645')

    def test_get_model_v0(self):
        """
        Tests fetching a v0 model.
        """
        path = get_model('10.5281/zenodo.8425684', path=self.temp_model.name)
        _check_file_in_model_dir(path, 'urdu_best.mlmodel', 16280146)

    def test_get_model_concept_doi_v0(self):
        """
        Tests fetching a v0 model by concept DOI.
        """
        path = get_model('10.5281/zenodo.8425683', path=self.temp_model.name)
        _check_file_in_model_dir(path, 'urdu_best.mlmodel', 16280146)

    def test_get_model_v1(self):
        """
        Tests fetching a v1 model.
        """
        path = get_model('10.5281/zenodo.14585602', path=self.temp_model.name)
        _check_file_in_model_dir(path, 'urdu_best.mlmodel', 16280146)

    def test_get_model_concept_doi_v1 (self):
        """
        Tests fetching a v1 model by concept DOI.
        """
        path = get_model('10.5281/zenodo.7051645', path=self.temp_model.name)
        _check_file_in_model_dir(path, 'urdu_best.mlmodel', 16280146)

    def test_prev_record_version_get_model_v0(self):
        """
        Tests fetching a model that has a superseding newer version.
        """
        path = get_model('10.5281/zenodo.6657809', path=self.temp_model.name)
        _check_file_in_model_dir(path, 'HTR-United-Manu_McFrench.mlmodel', 16176844)
