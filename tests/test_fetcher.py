from unittest.mock import Mock, patch

from django.test import TestCase

from simplecep.fetcher import get_cep_data


def dict_cache(path):
    return dict


@patch("simplecep.fetcher.fetch_from_providers")
@patch("simplecep.fetcher.import_string")
class FetcherTestCase(TestCase):
    def test_fetcher_should_get_from_cache_when_its_available(
        self, import_string_mock, fetch_from_providers_mock
    ):
        return_mock = Mock()
        import_string_mock.return_value.return_value = {"12345678": return_mock}

        self.assertEqual(get_cep_data("12345678"), return_mock)
        fetch_from_providers_mock.assert_not_called()

    def test_fetcher_should_get_from_providers_when_not_in_cache(
        self, import_string_mock, fetch_from_providers_mock
    ):
        fake_cache = {}
        import_string_mock.return_value.return_value = fake_cache
        self.assertEqual(
            get_cep_data("12345678"), fetch_from_providers_mock.return_value
        )
        import_string_mock.return_value.assert_called_once()
        # and save the fetched value into the cache
        self.assertEqual(fake_cache["12345678"], fetch_from_providers_mock.return_value)
