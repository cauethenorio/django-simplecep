from typing import Dict

from django.utils.module_loading import import_string

from .db_cache import CepDatabaseCache  # noqa
from ..conf import simplecep_settings


def get_installed_cache() -> Dict:
    CEPCache = import_string(simplecep_settings["CACHE"])
    return CEPCache()
