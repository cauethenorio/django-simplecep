from typing import Dict

from django.utils.module_loading import import_string

from .db_cache import CepDatabaseCache  # noqa
from ..conf import SETTINGS


def get_installed_cache() -> Dict:
    CEPCache = import_string(SETTINGS["CACHE"])
    return CEPCache()
