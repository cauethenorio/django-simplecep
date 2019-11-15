from json import loads
from typing import Optional

from .base import BaseCEPProvider, CEPAddress


class RepublicVirtualCEPProvider(BaseCEPProvider):
    def get_api_url(self, cep: str) -> str:
        return f"http://cep.republicavirtual.com.br/web_cep.php?cep={self.normalize_cep(cep)}&formato=json"

    def get_cep_data(self, cep: str) -> Optional[CEPAddress]:
        raw_fields = loads(
            self.request(self.get_api_url(cep), headers={"Accept": "application/json"})
        )

        if int(raw_fields["resultado"]) > 0:
            return self.convert_to_cep_address(raw_fields, self.normalize_cep(cep))
        return None

    def convert_to_cep_address(self, raw_fields, cep: str) -> CEPAddress:
        # remove empty string fields
        fields = {k: value.strip() for k, value in raw_fields.items() if value}

        if fields.get("logradouro") and fields.get("tipo_logradouro"):
            fields["street"] = f"{fields['tipo_logradouro']} {fields['logradouro']}"

        return CEPAddress(
            cep=cep,
            street=self.normalize_street(fields.get("street")),
            state=fields["uf"],
            neighborhood=fields.get("bairro"),
            city=fields["cidade"],
        )
