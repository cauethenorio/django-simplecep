import abc
import re
import socket
from urllib.request import urlopen, Request
from urllib.error import URLError

from typing import Optional, Dict

from ..conf import CEPAddress


class CepProviderFetchError(Exception):
    pass


class BaseCEPProvider(metaclass=abc.ABCMeta):

    # all providers should have an identifier */
    provider_id = None

    def __init__(self, timeout: float = None):
        self.timeout = timeout

    def request(
        self, url, method="GET", data=None, response_encoding="utf-8", headers=None
    ):
        """
        Helper function to perform HTTP requests
        """
        req = Request(url, data=data, method=method, headers=headers or {})
        try:
            return urlopen(req, timeout=self.timeout).read().decode(response_encoding)
        except (URLError, socket.timeout) as error:
            raise CepProviderFetchError(error)

    def clean_cep(self, cep: str) -> str:
        match = re.match("^(\\d{5})-?(\\d{3})$", cep)
        return "".join(match.groups())

    def clean_street(self, street: Optional[str]) -> Optional[str]:
        """
        Remove numbers from street names (i.e. post office agency CEPs)
        """
        if street is not None:
            match = re.match(r"^([^,]+),?\s\d+$", street)
            if match is not None:
                return match.groups()[0]
            return street

    def clean(self, fields: Dict) -> CEPAddress:
        fields = self.extract_district(fields)

        return CEPAddress(
            cep=self.clean_cep(fields["cep"]),
            state=fields["state"],
            city=fields["city"],
            neighborhood=fields.get("neighborhood"),
            street=self.clean_street(fields.get("street")),
        )

    def extract_district(self, original_fields: Dict):
        """
        Extract the district name from the city name and send it as neighborhood
        Example: 'Jaci Paraná (Porto Velho)' for 76840-000
        """
        fields = original_fields.copy()
        if fields.get("neighborhood") is None:
            match = re.match(r"^(.+)\s\((.+)\)$", fields["city"])
            if match:
                neighborhood, city = match.groups()
                fields["neighborhood"] = neighborhood
                fields["city"] = city
        return fields

    @abc.abstractmethod
    def get_cep_data(self, cep: str) -> Optional[CEPAddress]:
        """
        Return the CEP data
        """


# 38612-044 created in Feb 2019
# 38610-000 discarded in Feb 2019
