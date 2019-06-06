import os


def get_tests_cep_file_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "tests_ceps.txt.zip")
