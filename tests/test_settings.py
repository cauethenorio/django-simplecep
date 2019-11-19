from unittest import mock

from django.test import TestCase

from simplecep.conf import DEFAULT_SETTINGS, get_merged_settings


class SimpleCepSettingsTestCase(TestCase):
    def test_should_use_default_when_project_has_no_settings(self):
        self.assertEqual(DEFAULT_SETTINGS, get_merged_settings())

    def get_should_merge_when_project_has_partial_settings(self):
        PROJECT_CONFIG = {"PROVIDERS_TIMEOUT": mock.Mock(), "PROVIDERS": mock.Mock()}

        with self.settings(SIMPLECEP=PROJECT_CONFIG):
            merged = get_merged_settings()
            expected = DEFAULT_SETTINGS.copy()
            expected.update(PROJECT_CONFIG)
            self.assertEqual(merged, expected)
