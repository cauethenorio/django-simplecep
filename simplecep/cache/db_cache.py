import collections
from typing import Optional, Iterator

from simplecep.conf import CEPAddress


class CepDatabaseCache(collections.MutableMapping):
    """
    Dict-like class to read and store CEPs to database acting as CEP cache
    """

    @property
    def CachedCep(self):
        # we can't load django models on app setup
        # so we import it here when its used for real
        from simplecep.models import CachedCep

        return CachedCep

    def __getitem__(self, cep: str) -> Optional[CEPAddress]:
        try:
            return self.CachedCep.valid_ceps.get(cep=cep).to_cep_address()
        except self.CachedCep.DoesNotExist:
            raise KeyError

    def __setitem__(self, cep: str, cepaddress: CEPAddress) -> None:
        assert cep == cepaddress.cep, "Key should be the same as capaddress.cep"
        self.CachedCep.update_from_cep_address(cepaddress)

    def __delitem__(self, cep: str) -> None:
        try:
            cep_model = self.CachedCep.valid_ceps.get(cep=cep)
        except self.CachedCep.DoesNotExist:
            raise KeyError
        cep_model.delete()

    def __iter__(self) -> Iterator[CEPAddress]:
        for cep_model in self.CachedCep.valid_ceps.order_by("cep"):
            yield cep_model.to_cep_address()

    def __len__(self) -> int:
        return self.CachedCep.valid_ceps.count()
