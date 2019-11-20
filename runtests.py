#!/usr/bin/env python

import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

import coverage


if __name__ == "__main__":
    cov = coverage.Coverage(source=["simplecep"])
    cov.start()

    os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings"
    django.setup()

    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    params = sys.argv[1:]
    failures = test_runner.run_tests(
        params if len(params) else ["tests", "tests.providers"]
    )

    cov.stop()
    cov.save()

    sys.exit(bool(failures))
