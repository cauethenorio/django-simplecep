from django.test import TestCase

from simplecep import CEPAddress


class CEPAddressTestCase(TestCase):
    def get_cepaddress_sample(self):
        return CEPAddress(
            cep="00000111",
            street="Rua",
            state="XX",
            district="Centro",
            city="Rio Redondo",
            provider="fake",
        )

    def test_equals_should_be_true_only_exact_the_same(self):
        cep_address = self.get_cepaddress_sample()
        self.assertEqual(
            cep_address, CEPAddress(**cep_address.to_dict(with_provider=True))
        )
        self.assertNotEqual(cep_address, CEPAddress(**cep_address.to_dict()))
        self.assertNotEqual(cep_address, 1)
        self.assertNotEqual(cep_address, "")

    def test_repr_doesnt_raise(self):
        cep_address = self.get_cepaddress_sample()
        repr(cep_address)

    def test_assert_provider_is_not_in_generated_dict(self):
        cep_address = self.get_cepaddress_sample()
        self.assertFalse(hasattr(cep_address.to_dict(), "provider"))
