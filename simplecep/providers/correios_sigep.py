from typing import Dict, Optional
from xml.etree import cElementTree as ET

from .base import BaseCEPProvider, CEPAddress


class CorreiosSIGEPCEPProvider(BaseCEPProvider):
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
                     <cep>{self.normalize_cep(cep)}</cep>
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

    def convert_to_cep_address(self, fields) -> CEPAddress:
        return CEPAddress(
            cep=self.normalize_cep(fields["cep"]),
            state=fields.get("uf"),
            city=fields.get("cidade"),
            neighborhood=fields.get("bairro"),
            street=fields.get("end"),
        )

    def get_cep_data(self, cep: str) -> Optional[CEPAddress]:
        response = self.request(
            self.SIGEP_URL,
            data=self.envelope(cep),
            method="POST",
            response_encoding="latin1",
        )
        fields = self.unenvelope(response)
        if fields is not None:
            return self.convert_to_cep_address(fields)


resp = CorreiosSIGEPCEPProvider().get_cep_data("01001000")

if resp is not None:
    print(resp.__dict__)
else:
    print("None")
