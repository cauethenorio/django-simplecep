from django.forms.models import model_to_dict
from django.test import TestCase

from simplecep.models import Cep


class LoaderTestCase(TestCase):
    def test_migration_should_populate_db_with_ceps(self):
        db_value = [model_to_dict(row) for row in Cep.objects.order_by("cep")]
        self.assertListEqual(
            db_value,
            [
                {
                    "address": "Praça da Sé",
                    "cep": "01001000",
                    "city": "São Paulo",
                    "district": "Sé",
                    "extra": None,
                    "number": None,
                    "state": "SP",
                },
                {
                    "address": None,
                    "cep": "18170000",
                    "city": "Piedade",
                    "district": None,
                    "extra": None,
                    "number": None,
                    "state": "SP",
                },
                {
                    "address": "Avenida Presidente Castelo Branco",
                    "cep": "62880970",
                    "city": "Horizonte",
                    "district": "Centro",
                    "extra": " AC Horizonte",
                    "number": "4106 ",
                    "state": "CE",
                },
                {
                    "address": "Rodovia Mábio Gonçalves Palhano",
                    "cep": "86055991",
                    "city": "Londrina",
                    "district": None,
                    "extra": "CPC Patrimônio Regina",
                    "number": "s/n",
                    "state": "PR",
                },
            ],
        )

    def test_amigration_should_populate_db_with_ceps(self):
        pass
