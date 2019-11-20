from unittest.mock import patch

from django.urls import reverse
from django.test import TestCase

from .utils import TEST_DATA
from simplecep import CEPAddress, NoAvailableCepProviders


class ViewTestCase(TestCase):
    @patch("simplecep.views.get_cep_data")
    def test_view_existing_cep_should_return_cep_data(self, mocked_get_cep_data):
        for cep_data in TEST_DATA:
            mocked_get_cep_data.return_value = CEPAddress(
                cep=cep_data["cep"],
                state=cep_data["state"],
                city=cep_data["city"],
                neighborhood=cep_data["neighborhood"],
                street=cep_data["street"],
            )
            response = self.client.get(
                reverse("simplecep:get-cep", kwargs={"cep": cep_data["cep"]})
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), cep_data)

    @patch("simplecep.views.get_cep_data")
    def test_view_inexistent_cep_should_return_404_error(self, mocked_get_cep_data):
        mocked_get_cep_data.return_value = None
        response = self.client.get(
            reverse("simplecep:get-cep", kwargs={"cep": "00000000"})
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"error": "cep_not_found"})

    @patch("simplecep.views.get_cep_data")
    def test_view_should_return_error_when_no_providers_are_available(
        self, mocked_get_cep_data
    ):
        mocked_get_cep_data.side_effect = NoAvailableCepProviders()
        response = self.client.get(
            reverse("simplecep:get-cep", kwargs={"cep": "00000000"})
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"error": "no_cep_provider_available"})
