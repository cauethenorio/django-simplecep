from typing import Optional


class CEPAddress:
    """
    Represents an address fetched from a CEP number
    from cache or provider
    """

    cep: str
    street: Optional[str]
    state: str
    neighborhood: Optional[str]
    city: str

    def __init__(self, cep=None, state=None, city=None, neighborhood=None, street=None):
        self.cep = cep
        self.state = state
        self.city = city
        self.neighborhood = neighborhood
        self.street = street

    def __repr__(self):
        return f"<CEPAddress {self.cep}>"

    def to_dict(self):
        return {
            field: getattr(self, field)
            for field in "cep street state neighborhood city".split(" ")
        }


def get_cep_data(cep: str) -> Optional[CEPAddress]:
    # avoid loading models on app setup
    from simplecep.cache import get_installed_cache
    from simplecep.providers.fetcher import fetch_from_providers

    cep_cache = get_installed_cache()

    try:
        return cep_cache[cep]
    except KeyError:
        cep_address = fetch_from_providers(cep)
        if cep_address:
            cep_cache[cep] = cep_address
            return cep_address
