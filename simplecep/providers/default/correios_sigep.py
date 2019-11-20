from typing import Dict, Optional
from xml.etree import cElementTree as ET

from simplecep import CEPAddress
from simplecep.providers import BaseCEPProvider, CepProviderFetchError


class CorreiosSIGEPCEPProvider(BaseCEPProvider):
    # all providers should have a name */
    provider_id = "correios_sigep"

    SIGEP_URL = (
        "https://apps.correios.com.br/SigepMasterJPA/AtendeClienteService/AtendeCliente"
    )

    def envelope(self, cep: str) -> bytearray:
        return bytearray(
            f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cli="http://cliente.bean.master.sigep.bsb.correios.com.br/">
               <soapenv:Header/>
               <soapenv:Body>
                  <cli:consultaCEP>
                     <cep>{self.clean_cep(cep)}</cep>
                  </cli:consultaCEP>
               </soapenv:Body>
            </soapenv:Envelope>
        """.strip(),
            "ascii",
        )

    def unenvelope(self, response: str) -> Optional[Dict]:
        return_node = ET.fromstring(response).find(".//return")
        if return_node is not None:
            return {field.tag: field.text for field in return_node}
        return None

    def clean(self, fields) -> CEPAddress:
        return super().clean(
            {
                "cep": fields["cep"],
                "state": fields["uf"],
                "city": fields["cidade"],
                "neighborhood": fields.get("bairro"),
                "street": fields.get("end"),
            }
        )

    def is_cep_not_found_error(self, exc):
        """
        Check if the 500 response is about a not found CEP.
        We don't want throw errors for that.
        """
        if getattr(exc, "status", None) != 500:
            return False

        error_response = exc.read().decode("latin1")
        try:
            message = ET.fromstring(error_response).find(".//faultstring")
        except ET.ParseError:
            return False
        return message is not None and message.text in (
            "CEP INVÁLIDO",
            "CEP NAO ENCONTRADO",
        )

    def get_cep_data(self, cep: str) -> Optional[CEPAddress]:
        try:
            response = self.request(
                self.SIGEP_URL,
                data=self.envelope(cep),
                method="POST",
                response_encoding="latin1",
            )
        except CepProviderFetchError as e:
            original_exc = e.args[0]
            if self.is_cep_not_found_error(original_exc):
                return None
            raise

        fields = self.unenvelope(response)
        if fields is not None:
            return self.clean(fields)
