from contextlib import contextmanager
from unittest.mock import patch, Mock
from urllib.error import URLError


@contextmanager
def mock_urlopen():
    with patch("simplecep.providers.base.urlopen", autospec=True) as mock_urlopen:
        mock_response = Mock()
        mock_response.read.side_effect = [URLError("Network error")]
        mock_urlopen.return_value = mock_response
        yield


TEST_DATA = [
    {
        "street": "Praça da Sé",
        "cep": "01001000",
        "city": "São Paulo",
        "district": "Sé",
        "state": "SP",
    },
    {
        "street": None,
        "cep": "18170000",
        "city": "Piedade",
        "district": None,
        "state": "SP",
    },
    {
        "street": "Avenida Presidente Castelo Branco",
        "cep": "62880970",
        "city": "Horizonte",
        "district": "Centro",
        "state": "CE",
    },
    {
        "street": "Rodovia Mábio Gonçalves Palhano",
        "cep": "86055991",
        "city": "Londrina",
        "district": None,
        "state": "PR",
    },
]
