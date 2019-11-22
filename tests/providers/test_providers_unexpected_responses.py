from io import BytesIO
from unittest import mock
import socket
from urllib.response import addinfourl
from urllib.error import HTTPError, URLError

from django.test import TestCase

from simplecep.providers import CepProviderFetchError
from simplecep.providers.fetcher import providers


class ProvidersUnexpectedResponsesTestCase(TestCase):
    def assert_fetcherror_is_raised_when(self, error=None, response=None):
        def fake_urlopen(*args, **kwargs):
            if error is not None:
                raise error
            return response

        with mock.patch("simplecep.providers.base.urlopen", side_effect=fake_urlopen):
            for provider in providers:
                with self.subTest(provider=provider.__class__.__name__):
                    with self.assertRaises(CepProviderFetchError):
                        provider.get_cep_data("12345689")

    def test_providers_timeout_should_raise_proper_error(self):
        self.assert_fetcherror_is_raised_when(error=socket.timeout)

    def test_providers_dns_error_should_raise_proper_error(self):
        dns_error = URLError(
            "gaierror(8, 'nodename nor servname provided, or not known')",
        )
        self.assert_fetcherror_is_raised_when(error=dns_error)

    def test_providers_gateway_timeout_should_raise_proper_error(self):
        gateway_timeout_error = HTTPError(
            "https://fake-url.exampple.com",
            504,
            "Fake Gateway Timeout Error",
            {},
            BytesIO(b"<html>Gateway Timeout</html>"),
        )
        self.assert_fetcherror_is_raised_when(error=gateway_timeout_error)

    def test_fake_success_response_raise_proper_error(self):
        fake_success_response = addinfourl(
            BytesIO(b"Unexpected Content Here " + bytes(range(256))),
            {},
            "https://fake-url.exampple.com",
        )
        self.assert_fetcherror_is_raised_when(response=fake_success_response)

    def test_webserver_error_raise_proper_error(self):
        webserver_error = HTTPError(
            "https://fake-url.exampple.com",
            500,
            "Webserver Error",
            {},
            BytesIO(b"<html>I'm misconfigured" + bytes(range(256)) + b"</html>"),
        )
        self.assert_fetcherror_is_raised_when(error=webserver_error)
