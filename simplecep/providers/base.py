import abc
import re
from urllib.request import urlopen, Request

from typing import Optional


class CEPAddress:
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

    def to_dict(self):
        return self.__dict__


class BaseCEPProvider(metaclass=abc.ABCMeta):
    def __init(self):
        pass

    def request(
        self, url, method="GET", data=None, response_encoding="utf-8", headers=None
    ):
        """
        Helper function to perform HTTP requests
        """
        req = Request(url, data=data, method=method, headers=headers or {})
        return urlopen(req, timeout=2).read().decode(response_encoding)

    def normalize_cep(self, cep: str) -> str:
        match = re.match("^(\\d{5})-?(\\d{3})$", cep)
        return "".join(match.groups())

    @abc.abstractmethod
    def get_cep_data(self, cep: str) -> Optional[CEPAddress]:
        """
        Return the CEP data
        """


# 38612-044 created in Feb 2019
# 38610-000 discarded in Feb 2019
