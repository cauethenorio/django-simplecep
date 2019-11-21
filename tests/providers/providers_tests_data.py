"""
This file data is used in both files:
- capture_real_responses.py
- test_providers_data.py

The "capture_real_responses.py" script sends this data input keys values to
installed providers and store the responses in the "captured_responses.py" file.

The "test_providers_data.py" test case read this data as tests inputs,
uses the "captured_responses.py" file data to simulate the providers responses
and compare the providers outputs with the "expected_result" keys values.

If you change this data, run "capture_real_responses.py" to update the
"captured_responses.py" file content.
"""

providers_tests_data = [
    {
        "input": "01001000",
        "expected_result": {
            "cep": "01001000",
            "state": "SP",
            "city": "São Paulo",
            "district": "Sé",
            "street": "Praça da Sé",
        },
    },
    {
        "input": "57010-240",
        "expected_result": {
            "cep": "57010240",
            "state": "AL",
            "city": "Maceió",
            "district": "Prado",
            "street": "Rua Desembargador Inocêncio Lins",
        },
    },
    {
        "input": "18170000",
        "expected_result": {
            "cep": "18170000",
            "state": "SP",
            "city": "Piedade",
            "district": None,
            "street": None,
        },
    },
    {
        "input": "78175-000",
        "expected_result": {
            "cep": "78175000",
            "state": "MT",
            "city": "Poconé",
            "district": None,
            "street": None,
        },
    },
    {
        "input": "63200-970",
        "expected_result": {
            "cep": "63200970",
            "state": "CE",
            "city": "Missão Velha",
            "district": "Centro",
            "street": "Rua José Sobreira da Cruz",
        },
    },
    {
        "input": "69096-970",
        "expected_result": {
            "cep": "69096970",
            "state": "AM",
            "city": "Manaus",
            "district": "Cidade Nova",
            "street": "Avenida Noel Nutels",
        },
    },
    {
        "input": "20010-974",
        "expected_result": {
            "cep": "20010974",
            "state": "RJ",
            "city": "Rio de Janeiro",
            "district": "Centro",
            "street": "Rua Primeiro de Março",
        },
    },
    {
        "input": "96010-900",
        "expected_result": {
            "cep": "96010900",
            "state": "RS",
            "city": "Pelotas",
            "district": "Centro",
            "street": "Rua Tiradentes",
        },
    },
    {
        "input": "38101990",
        "expected_result": {
            "cep": "38101990",
            "state": "MG",
            "city": "Uberaba",
            "district": "Baixa",
            "street": "Rua Basílio Eugênio dos Santos",
        },
    },
    {
        "input": "76840-000",
        "expected_result": {
            "cep": "76840000",
            "state": "RO",
            "city": "Porto Velho",
            "district": "Jaci Paraná",
            "street": None,
        },
    },
    {
        "input": "86055991",
        "expected_result": {
            "cep": "86055991",
            "city": "Londrina",
            "district": None,
            "state": "PR",
            "street": "Rodovia Mábio Gonçalves Palhano",
        },
    },
    {"input": "00000000", "expected_result": None},
    {"input": "11111111", "expected_result": None},
    {"input": "99999999", "expected_result": None},
    {"input": "01111110", "expected_result": None},
]
