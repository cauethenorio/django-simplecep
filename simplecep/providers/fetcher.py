from typing import Optional

from simplecep import CEPAddress
from simplecep.providers import CepProviderFetchError, get_installed_providers


providers = get_installed_providers()


class NoAvailableCepProviders(Exception):
    pass


def fetch_from_providers(cep: str) -> Optional[CEPAddress]:
    for provider in providers:
        try:
            return provider.get_cep_data(cep)
        except CepProviderFetchError:
            pass
    raise NoAvailableCepProviders("No CEP Provider available at this time")
