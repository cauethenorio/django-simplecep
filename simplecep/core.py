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
