from django.test import TestCase

from simplecep.models import Cep
from simplecep.loader import load_base_ceps


class SampleTestCase(TestCase):
    def test_unit_sample(self):
        load_base_ceps(Cep)
