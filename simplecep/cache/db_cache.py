import collections
from typing import Optional, Iterator

from simplecep import CEPAddress
from simplecep.models import CachedCep


class CepDatabaseCache(collections.MutableMapping):
    """
    Dict-like class to read and store CEPs to database acting as CEP cache
    """

    def __getitem__(self, cep: str) -> Optional[CEPAddress]:
        try:
            return CachedCep.valid_ceps.get(cep=cep).to_cep_address()
        except CachedCep.DoesNotExist:
            raise KeyError

    def __setitem__(self, cep: str, cepaddress: CEPAddress) -> None:
        assert cep == cepaddress.cep, "Key should be the same as capaddress.cep"
        CachedCep.update_from_cep_address(cepaddress)

    def __delitem__(self, cep: str) -> None:
        try:
            cep_model = CachedCep.valid_ceps.get(cep=cep)
        except CachedCep.DoesNotExist:
            raise KeyError
        cep_model.delete()

    def __iter__(self) -> Iterator[CEPAddress]:
        for cep_model in CachedCep.valid_ceps.order_by("cep"):
            yield cep_model.to_cep_address()

    def __len__(self) -> int:
        return CachedCep.valid_ceps.count()
