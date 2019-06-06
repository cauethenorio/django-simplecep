import os
import sys
from unittest.mock import patch

import django
from django.conf import settings
from django.test.utils import get_runner

from tests import utils

if __name__ == "__main__":
    os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings"
    django.setup()

    mock = patch(
        "simplecep.loader.get_cep_file_path",
        return_value=utils.get_tests_cep_file_path(),
    )
    mock.start()
    utils.get_cep_file_path_mock = mock

    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    params = sys.argv[1:]
    failures = test_runner.run_tests(params if len(params) else ["tests"])
    sys.exit(bool(failures))
