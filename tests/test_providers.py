from django.test import TestCase

from simplecep.providers import (
    CorreiosSIGEPCEPProvider,
    RepublicVirtualCEPProvider,
    ViaCEPProvider,
)


class ProvidersTestCase(TestCase):
    providers = (CorreiosSIGEPCEPProvider, RepublicVirtualCEPProvider, ViaCEPProvider)

    def assert_providers_return_cep_address(self, cep, expected):
        for Provider in self.providers:
            with self.subTest(provider=Provider):
                cep_address = Provider().get_cep_data(cep)
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
