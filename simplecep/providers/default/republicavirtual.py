from json import loads, JSONDecodeError
from typing import Optional

from simplecep import CEPAddress
from simplecep.providers import BaseCEPProvider, CepProviderFetchError


class RepublicaVirtualCEPProvider(BaseCEPProvider):
    # all providers should have an identifier */
    provider_id = "republicavirtual"

    def get_api_url(self, cep: str) -> str:
        return f"http://cep.republicavirtual.com.br/web_cep.php?cep={self.clean_cep(cep)}&formato=json"

    def get_cep_data(self, cep: str) -> Optional[CEPAddress]:
        try:
            raw_fields = loads(
                self.request(
                    self.get_api_url(cep), headers={"Accept": "application/json"}
                )
            )
        except JSONDecodeError as e:
            raise CepProviderFetchError(e)

        if int(raw_fields["resultado"]) > 0:
            return self.clean_and_add_cep(raw_fields, cep)
        return None

    def clean_state(self, state: str) -> str:
        """
        Republica Virtual API returns a different state value when searching
        for a district address. (i.e. "RO  - Distrito" for 76840-000).
        So let's clean it!
        """
        return state.split(" ")[0].strip()

    def clean_and_add_cep(self, raw_fields, cep: str) -> CEPAddress:
        # remove empty string fields
        fields = {
            k: value.strip()
            for k, value in raw_fields.items()
            if value is not None and value.strip()
        }

        if fields.get("logradouro") and fields.get("tipo_logradouro"):
            fields["street"] = f"{fields['tipo_logradouro']} {fields['logradouro']}"

        return self.clean(
            {
                "cep": cep,
                "state": self.clean_state(fields["uf"]),
                "city": fields["cidade"],
                "district": fields.get("bairro"),
                "street": fields.get("street"),
            }
        )
