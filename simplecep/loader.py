import itertools
import os
import sys
from typing import Iterable, Any
import zipfile

fields = ["cep", "state", "city", "district", "address", "number", "extra"]


def get_cep_file_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "cep-data", "ceps.txt.zip")


def read_cep_file_by_path(path: str):
    with zipfile.ZipFile(path) as zf:
        with zf.open("ceps.txt") as cep_fp:
            for line in cep_fp:
                values = [v or None for v in line.strip().decode("utf-8").split("\t")]
                yield dict(zip(fields, values))


def read_cep_file():
    return read_cep_file_by_path(get_cep_file_path())


def grouper(n: int, iterable: Iterable[Any]) -> Iterable[Iterable[Any]]:
    """
    >>> list(grouper(3, 'ABCDEFG'))
    [['A', 'B', 'C'], ['D', 'E', 'F'], ['G']]
    """
    iterable = iter(iterable)
    return iter(lambda: list(itertools.islice(iterable, n)), [])


def read_cep_file_in_batches(batch_size: int = 1000):
    message = "Importing CEPs"
    return grouper(batch_size, show_counter(read_cep_file(), message))


class show_counter:
    def __init__(
        self, iterable: Iterable[Any], message_prefix: str, update_interval: int = 1000
    ):
        self.message_prefix = message_prefix
        self.update_interval = update_interval
        self.counter = 0
        self.iterable = iterable

    def print(self):
        print(f"\r{self.message_prefix}... {self.counter:>10}", end="")
        sys.stdout.flush()

    def __iter__(self):
        for item in self.iterable:
            yield item
            self.counter += 1

            if self.counter > 0 and self.counter % self.update_interval == 0:
                self.print()
        self.print()


def load_base_ceps(CepModel):
    for cep_data_batch in read_cep_file_in_batches():
        ceps = [CepModel(**cep_data) for cep_data in cep_data_batch]
        CepModel.objects.bulk_create(ceps)
