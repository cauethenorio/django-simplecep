from typing import Optional, Any


class CEPAddress:
    """
    Represents an address fetched from a CEP number
    from cache or provider
    """

    cep: str
    state: str
    district: Optional[str]
    street: Optional[str]
    city: str
    provider: str

    _data_fields = "cep street state district city provider".split(" ")

    def __init__(
        self, cep=None, state=None, city=None, district=None, street=None, provider=None
    ):
        self.cep = cep
        self.state = state
        self.city = city
        self.district = district
        self.street = street
        self.provider = provider

    def __repr__(self):
        return f"<CEPAddress {self.cep}>"

    def __eq__(self, other: Any):
        if not isinstance(other, CEPAddress):
            return False

        return all(getattr(self, f) == getattr(other, f) for f in self._data_fields)

    def to_dict(self, with_provider=False):
        data_fields = self._data_fields.copy()
        if not with_provider:
            data_fields.remove("provider")

        return {field: getattr(self, field) for field in data_fields}
