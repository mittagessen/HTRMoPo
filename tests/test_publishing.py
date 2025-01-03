# -*- coding: utf-8 -*-
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from jsonschema.exceptions import ValidationError

thisfile = Path(__file__).resolve().parent
resources = thisfile / 'resources'


@patch.dict(os.environ, {'MODEL_REPO_URL': 'https://sandbox.zenodo.org/api/'})
class TestPublishing(unittest.TestCase):
    """
    Testing interaction with the model repository.
    """

    def setUp(self):
        if (access_token := os.getenv('ZENODO_ACCESS_TOKEN', None)) is None:
            raise unittest.SkipTest('No Zenodo API access token available')
        else:
            self.access_token = access_token

        with open(resources / 'llama_party.md', 'r') as fp:
            self.model_card = fp.read()

        with open(resources / 'invalid_party.md', 'r') as fp:
            self.invalid_model_card = fp.read()

        self.model_path = resources / 'test_model'

    def test_publish(self):
        """
        Tests publishing a model
        """
        from htrmopo import publish_model
        doi = publish_model(model=self.model_path,
                            model_card=self.model_card,
                            access_token=self.access_token)

    def test_invalid_publish(self):
        """
        Tests publishing a model with an invalid model card.
        """
        from htrmopo import publish_model
        with self.assertRaises(ValidationError):
            _ = publish_model(model=self.model_path,
                              model_card=self.invalid_model_card,
                              access_token=self.access_token)

    def test_update(self):
        """
        Tests updating a model
        """
        from htrmopo import update_model, publish_model
        doi = publish_model(model=self.model_path,
                            model_card=self.model_card,
                            access_token=self.access_token)

        doi = update_model(model_id=doi,
                           model=self.model_path,
                           model_card=self.model_card,
                           access_token=self.access_token)

    def test_invalid_metadata_update(self):
        """
        Tests updating a model with an invalid model card.
        """
        from htrmopo import publish_model, update_model
        with self.assertRaises(ValidationError):
            doi = publish_model(model=self.model_path,
                                model_card=self.model_card,
                                access_token=self.access_token)

            _ = update_model(model_id=doi,
                             model=self.model_path,
                             model_card=self.invalid_model_card,
                             access_token=self.access_token)

    def test_invalid_base_record_update(self):
        """
        Tests updating a model with an concept/prior record DOI
        """
        from htrmopo import publish_model, update_model
        with self.assertRaises(ValidationError):
            doi = publish_model(model=self.model_path,
                                model_card=self.model_card,
                                access_token=self.access_token)

            _ = update_model(model_id=doi,
                             model=self.model_path,
                             model_card=self.invalid_model_card,
                             access_token=self.access_token)


