from typing import Optional, Dict

from django.utils.module_loading import import_string

from simplecep import CEPAddress
from simplecep.conf import simplecep_settings
from simplecep.providers import fetch_from_providers


def get_installed_cache() -> Dict:
    CEPCache = import_string(simplecep_settings["CACHE"])
    return CEPCache()


def get_cep_data(cep: str) -> Optional[CEPAddress]:
    cep_cache = get_installed_cache()
    try:
        return cep_cache[cep]
    except KeyError:
        cep_address = fetch_from_providers(cep)
        if cep_address:
            cep_cache[cep] = cep_address
            return cep_address
