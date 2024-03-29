from json import loads, JSONDecodeError
from typing import Optional

from simplecep import CEPAddress
from simplecep.providers import BaseCEPProvider, CepProviderFetchError


class ViaCEPProvider(BaseCEPProvider):
    # all providers should have an identifier */
    provider_id = "viacep"

    def get_api_url(self, cep: str) -> str:
        return f"https://viacep.com.br/ws/{self.clean_cep(cep)}/json/unicode/"

    def get_cep_data(self, cep: str) -> Optional[CEPAddress]:
        try:
            raw_fields = loads(self.request(self.get_api_url(cep)))
        except JSONDecodeError as e:
            raise CepProviderFetchError(e)

        if raw_fields.get("erro") is not True:
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
                "district": fields.get("bairro"),
                "street": fields.get("logradouro"),
            }
        )
