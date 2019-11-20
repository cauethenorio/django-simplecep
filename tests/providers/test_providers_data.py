from io import BytesIO
from pprint import pformat
from unittest import mock
from urllib.response import addinfourl
from urllib.error import HTTPError

from django.test import TestCase

from simplecep.providers.fetcher import providers
from .providers_tests_data import providers_tests_data
from .captured_responses import captured_responses


def patched_urlopen(req, timeout):
    """"
    A customized version of urlopen which will take the responses from
    the captured_responses.py file instead of triggering real HTTP requests.
    """
    req_dict = {
        "full_url": req.full_url,
        "method": req.method,
        "headers": req.headers,
        "data": req.data,
    }

    for messages in captured_responses:
        if messages["request"] == req_dict:
            response = messages["response"]

            if response["type"] == "success":
                # Create a fake response object with the same data was captured
                # from the real endpoint
                return addinfourl(BytesIO(response["data"]), {}, req_dict["full_url"])
            elif response["type"] == "error":
                # Create a fake response error object with the same data
                # captured from the real endpoint
                raise HTTPError(
                    req_dict["full_url"],
                    response["status"],
                    "Fake Error",
                    {},
                    BytesIO(response["data"]),
                )

    raise ValueError(
        f"No stored response found for:\n {pformat(req_dict)} request.\n\n"
        "Please run the script to capture real providers responses with:\n"
        "$ python -m tests.providers.capture_real_responses\n\nAnd try again."
    )


class ProvidersDataTestCase(TestCase):
    def test_valid_complete_cep(self):
        # bye real urlopen and welcome our patched version which skips
        # real requests and return captured_responses.py file content
        with mock.patch(
            "simplecep.providers.base.urlopen", side_effect=patched_urlopen
        ):
            for test_data in providers_tests_data:
                cep = test_data["input"]
                expected_result = test_data["expected_result"]
                with self.subTest(test_data=test_data):
                    for provider in providers:
                        with self.subTest(provider=provider.__class__.__name__):
                            cep_address = provider.get_cep_data(cep)
                            if expected_result is None:
                                self.assertEqual(cep_address, expected_result)
                            else:
                                self.assertEqual(cep_address.to_dict(), expected_result)
