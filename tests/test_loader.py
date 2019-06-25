from django.forms.models import model_to_dict
from django.urls import reverse
from django.test import TestCase, Client

from simplecep.models import Cep
from .utils import TEST_DATA


class LoaderTestCase(TestCase):
    def test_migration_should_populate_db_with_ceps(self):
        db_value = [model_to_dict(row) for row in Cep.objects.order_by("cep")]
        self.assertListEqual(db_value, TEST_DATA)
