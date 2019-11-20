from unittest import mock

from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured

from simplecep.providers import (
    BaseCEPProvider,
    CepProviderFetchError,
    get_installed_providers,
    fetch_from_providers,
    NoAvailableCepProviders,
)


class SimpleCepSettingsTestCase(TestCase):
    @mock.patch("simplecep.providers.get_installed.import_string", autospec=True)
    def test_valid_providers_instantiation_should_work(self, mocked_import_string):
        timeout_config_mock = mock.Mock()
        providers_classes_mock = [
            mock.Mock(spec=BaseCEPProvider),
            mock.Mock(spec=BaseCEPProvider),
            mock.Mock(spec=BaseCEPProvider),
        ]
        mocked_import_string.side_effect = providers_classes_mock

        with mock.patch.dict(
            "simplecep.providers.get_installed.simplecep_settings",
            {"PROVIDERS_TIMEOUT": timeout_config_mock},
        ):
            providers = get_installed_providers()

        for provider_class_mock in providers_classes_mock:
            provider_class_mock.assert_called_once_with(timeout_config_mock)

        self.assertListEqual(
            providers, [m.return_value for m in providers_classes_mock]
        )

    @mock.patch("simplecep.providers.get_installed.import_string", autospec=True)
    def test_providers_without_provider_id_should_error_out(self, mocked_import_string):
        # mocks a provider class without the provider_id attr
        providers_classes_mock = [mock.Mock(return_value=mock.Mock(spec=[]))]
        mocked_import_string.side_effect = providers_classes_mock
        with self.assertRaises(ImproperlyConfigured):
            get_installed_providers()

    @mock.patch("simplecep.providers.get_installed.import_string", autospec=True)
    def test_duplicated_provider_ids_should_error_out(self, mocked_import_string):

        providers_classes_mock = [
            mock.Mock(return_value=mock.Mock(provider_id="repeated")),
            mock.Mock(return_value=mock.Mock(provider_id="repeated")),
        ]
        mocked_import_string.side_effect = providers_classes_mock
        with self.assertRaises(ImproperlyConfigured):
            get_installed_providers()

    def fill_providers_mock_with(self, providers_mock, providers_types):
        providers_type_map = {
            "valid": mock.Mock(get_cep_data=mock.Mock()),
            "unavailable": mock.Mock(
                get_cep_data=mock.Mock(side_effect=CepProviderFetchError())
            ),
        }
        providers_mock.__iter__.return_value = [
            providers_type_map[provider_type] for provider_type in providers_types
        ]
        return providers_type_map.values()

    @mock.patch("simplecep.providers.fetcher.providers", autospec=True)
    def test_all_providers_should_be_tried_until_a_working_one(self, providers_mock):
        valid_mock, unavailable_mock, = self.fill_providers_mock_with(
            providers_mock, ["unavailable", "unavailable", "valid"]
        )

        self.assertEqual(fetch_from_providers(""), valid_mock.get_cep_data.return_value)
        self.assertEqual(unavailable_mock.get_cep_data.call_count, 2)
        valid_mock.get_cep_data.assert_called_once()

    @mock.patch("simplecep.providers.fetcher.providers", autospec=True)
    def test_subsequent_providers_should_not_be_run_after_a_working_one(
        self, providers_mock
    ):
        valid_mock, unavailable_mock, = self.fill_providers_mock_with(
            providers_mock, ["valid", "unavailable", "unavailable"]
        )
        self.assertEqual(fetch_from_providers(""), valid_mock.get_cep_data.return_value)
        valid_mock.get_cep_data.assert_called_once()
        unavailable_mock.assert_not_called()

    @mock.patch("simplecep.providers.fetcher.providers", autospec=True)
    def test_call_providers_until_finding_a_working_one(self, providers_mock):
        valid_mock, unavailable_mock, = self.fill_providers_mock_with(
            providers_mock, ["unavailable", "valid", "unavailable"]
        )
        self.assertEqual(fetch_from_providers(""), valid_mock.get_cep_data.return_value)
        valid_mock.get_cep_data.assert_called_once()
        unavailable_mock.get_cep_data.assert_called_once()

    @mock.patch("simplecep.providers.fetcher.providers", autospec=True)
    def test_no_available_providers_should_raise(self, providers_mock):
        valid_mock, unavailable_mock, = self.fill_providers_mock_with(
            providers_mock, ["unavailable", "unavailable", "unavailable"]
        )
        with self.assertRaises(NoAvailableCepProviders):
            fetch_from_providers("")
        self.assertEqual(unavailable_mock.get_cep_data.call_count, 3)
