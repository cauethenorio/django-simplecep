from django.urls import reverse
from django.test import TestCase, Client

from .utils import TEST_DATA


class ViewTestCase(TestCase):
    def test_view_should_return_cep_data(self):
        self.client = Client()

        for cep_data in TEST_DATA:
            response = self.client.get(
                reverse("simplecep:get-cep", kwargs={"cep": cep_data["cep"]})
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), cep_data)

    def test_wrong_cep_should_return_404_error(self):
        response = self.client.get(
            reverse("simplecep:get-cep", kwargs={"cep": "00000000"})
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"error": "cep_not_found"})
