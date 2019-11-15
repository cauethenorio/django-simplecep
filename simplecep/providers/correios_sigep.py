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

    def get_cep_data(self, cep: str) -> Optional[CEPAddress]:
        response = self.request(
            self.SIGEP_URL,
            data=self.envelope(cep),
            method="POST",
            response_encoding="latin1",
        )
        fields = self.unenvelope(response)
        if fields is not None:
            return self.clean(fields)
