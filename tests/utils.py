import os


def get_tests_cep_file_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "tests_ceps.txt.zip")


TEST_DATA = [
    {
        "address": "Praça da Sé",
        "cep": "01001000",
        "city": "São Paulo",
        "district": "Sé",
        "extra": None,
        "number": None,
        "state": "SP",
    },
    {
        "address": None,
        "cep": "18170000",
        "city": "Piedade",
        "district": None,
        "extra": None,
        "number": None,
        "state": "SP",
    },
    {
        "address": "Avenida Presidente Castelo Branco",
        "cep": "62880970",
        "city": "Horizonte",
        "district": "Centro",
        "extra": " AC Horizonte",
        "number": "4106 ",
        "state": "CE",
    },
    {
        "address": "Rodovia Mábio Gonçalves Palhano",
        "cep": "86055991",
        "city": "Londrina",
        "district": None,
        "extra": "CPC Patrimônio Regina",
        "number": "s/n",
        "state": "PR",
    },
]
