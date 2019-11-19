from django.test import TestCase

from simplecep.providers import (
    CorreiosSIGEPCEPProvider,
    RepublicaVirtualCEPProvider,
    ViaCEPProvider,
)


class ProvidersTestCase(TestCase):
    """
    This TestCase make real requests to default providers to assure all values
    are being correctly normalized and the app code is sync with APIs responses
    format.

    It doesn't run by default when running the test suite. To run it call:
    ./runtests.py tests.heavy_test_providers_in_the_wild
    """

    providers = (CorreiosSIGEPCEPProvider, RepublicaVirtualCEPProvider, ViaCEPProvider)

    def assert_providers_return_cep_address(self, cep, expected):
        for Provider in self.providers:
            with self.subTest(provider=Provider):
                cep_address = Provider().get_cep_data(cep)
                if expected is None:
                    self.assertEqual(cep_address, expected)
                else:
                    self.assertEqual(cep_address.to_dict(), expected)

    def test_valid_complete_cep(self):
        self.assert_providers_return_cep_address(
            "01001000",
            {
                "cep": "01001000",
                "state": "SP",
                "city": "São Paulo",
                "neighborhood": "Sé",
                "street": "Praça da Sé",
            },
        )
        self.assert_providers_return_cep_address(
            "57010-240",
            {
                "cep": "57010240",
                "state": "AL",
                "city": "Maceió",
                "neighborhood": "Prado",
                "street": "Rua Desembargador Inocêncio Lins",
            },
        )

    def test_valid_partial_cep(self):
        self.assert_providers_return_cep_address(
            "18170000",
            {
                "cep": "18170000",
                "state": "SP",
                "city": "Piedade",
                "neighborhood": None,
                "street": None,
            },
        )
        self.assert_providers_return_cep_address(
            "78175-000",
            {
                "cep": "78175000",
                "state": "MT",
                "city": "Poconé",
                "neighborhood": None,
                "street": None,
            },
        )

    def test_valid_postoffice_agency_cep(self):
        self.assert_providers_return_cep_address(
            "63200-970",
            {
                "cep": "63200970",
                "state": "CE",
                "city": "Missão Velha",
                "neighborhood": "Centro",
                "street": "Rua José Sobreira da Cruz",
            },
        )
        self.assert_providers_return_cep_address(
            "69096-970",
            {
                "cep": "69096970",
                "state": "AM",
                "city": "Manaus",
                "neighborhood": "Cidade Nova",
                "street": "Avenida Noel Nutels",
            },
        )

    def test_valid_mailbox_cep(self):
        self.assert_providers_return_cep_address(
            "20010-974",
            {
                "cep": "20010974",
                "state": "RJ",
                "city": "Rio de Janeiro",
                "neighborhood": "Centro",
                "street": "Rua Primeiro de Março",
            },
        )
        self.assert_providers_return_cep_address(
            "96010-900",
            {
                "cep": "96010900",
                "state": "RS",
                "city": "Pelotas",
                "neighborhood": "Centro",
                "street": "Rua Tiradentes",
            },
        )

    def test_valid_cep_with_district_should_be_normalized(self):
        self.assert_providers_return_cep_address(
            "38101990",
            {
                "cep": "38101990",
                "state": "MG",
                "city": "Uberaba",
                "neighborhood": "Baixa",
                "street": "Rua Basílio Eugênio dos Santos",
            },
        )
        self.assert_providers_return_cep_address(
            "76840-000",
            {
                "cep": "76840000",
                "state": "RO",
                "city": "Porto Velho",
                "neighborhood": "Jaci Paraná",
                "street": None,
            },
        )

    def test_inexistent_cep_should_return_none(self):
        self.assert_providers_return_cep_address("00000000", None)
        self.assert_providers_return_cep_address("11111111", None)
        self.assert_providers_return_cep_address("99999999", None)
        self.assert_providers_return_cep_address("01111110", None)
