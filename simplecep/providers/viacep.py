from json import loads
from typing import Optional

from .base import BaseCEPProvider, CEPAddress


class ViaCEPProvider(BaseCEPProvider):
    def get_api_url(self, cep: str) -> str:
        return f"https://viacep.com.br/ws/{self.clean_cep(cep)}/json/unicode/"

    def get_cep_data(self, cep: str) -> Optional[CEPAddress]:
        raw_fields = loads(self.request(self.get_api_url(cep)))
        if raw_fields.get("erro") != True:
            return self.clean(raw_fields)
        return None

    def clean(self, raw_fields) -> CEPAddress:
        # remove empty string fields
        fields = {k: value for k, value in raw_fields.items() if value}

        return super().clean(
            {
                "cep": fields["cep"],
                "state": fields["uf"],
                "city": fields["localidade"],
                "neighborhood": fields.get("bairro"),
                "street": fields.get("logradouro"),
            }
        )
