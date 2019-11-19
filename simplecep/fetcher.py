from typing import Optional

from .conf import CEPAddress
from .cache import get_installed_cache
from .providers import get_installed_providers, CepProviderFetchError


providers = get_installed_providers()
cep_cache = get_installed_cache()


class NoCepProviderAvailable(Exception):
    pass


def fetch_from_providers(cep: str) -> Optional[CEPAddress]:
    for provider in providers:
        try:
            return provider.get_cep_data(cep)
        except CepProviderFetchError:
            pass
    raise NoCepProviderAvailable("No CEP Provider available at the moment")


def get_cep_data(cep: str) -> Optional[CEPAddress]:
    try:
        return cep_cache[cep]
    except KeyError:
        cep_address = fetch_from_providers(cep)
        if cep_address:
            cep_cache[cep] = cep_address
            return cep_address
