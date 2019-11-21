from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from simplecep.cache import CepDatabaseCache
from simplecep.conf import simplecep_settings
from simplecep.models import CepCache
from simplecep import CEPAddress


class CepDatabaseCacheTestCase(TestCase):
    def get_sample_cep_address(self, cep="10000001"):
        return CEPAddress(
            cep=cep,
            street="Rua",
            state="XX",
            district="Centro",
            city="Rio Redondo",
            provider="fake",
        )

    def create_ceps_in_db(self, num_to_create=1):
        created = []
        for n in range(num_to_create):
            cep = "{:0>8}".format(n)
            cep_address = self.get_sample_cep_address(cep=cep)
            CepCache.update_from_cep_address(cep_address)
            created.append(cep_address)
        return created

    def assert_num_ceps_in_db(self, num: int) -> None:
        self.assertEqual(CepCache.valid_ceps.count(), num)

    def test_assigning_should_add_to_cache(self):
        db_cache = CepDatabaseCache()
        sample_cep_address = self.get_sample_cep_address()
        db_cache["10000001"] = sample_cep_address
        self.assert_num_ceps_in_db(1)
        self.assertEqual(
            CepCache.valid_ceps.first().to_cep_address(), sample_cep_address,
        )

    def test_assigning_with_wrong_cep_value_should_raise(self):
        db_cache = CepDatabaseCache()
        sample_cep_address = self.get_sample_cep_address()
        with self.assertRaises(AssertionError):
            db_cache["10000002"] = sample_cep_address

    def test_getting_should_read_from_cache(self):
        db_cache = CepDatabaseCache()
        (cep_address,) = self.create_ceps_in_db(1)

        self.assert_num_ceps_in_db(1)
        self.assertEqual(
            db_cache[cep_address.cep], CepCache.valid_ceps.first().to_cep_address(),
        )

    def test_getting_inexistent_should_raise_keyerror(self):
        db_cache = CepDatabaseCache()
        with self.assertRaises(KeyError):
            _ = db_cache["10000001"]

    def test_deleting_should_remove_from_cache(self):
        db_cache = CepDatabaseCache()
        (cep_address,) = self.create_ceps_in_db(1)
        self.assert_num_ceps_in_db(1)
        del db_cache[cep_address.cep]
        self.assert_num_ceps_in_db(0)

    def test_iterating_should_read_all_cache_items(self):
        (sample1, sample2) = self.create_ceps_in_db(2)
        db_cache = CepDatabaseCache()
        ceps_list = [c.cep for c in db_cache]
        self.assertListEqual(ceps_list, [sample1.cep, sample2.cep])

    def test_len_should_count_all_cache_items(self):
        db_cache = CepDatabaseCache()
        self.create_ceps_in_db(3)
        self.assertEqual(len(db_cache), 3)

    def test_stale_cep_should_be_skiped_by_cache(self):
        db_cache = CepDatabaseCache()
        (sample_cep,) = self.create_ceps_in_db(1)
        self.assertIsNotNone(db_cache[sample_cep.cep])

        timeout_limit = timezone.now() - simplecep_settings["CEP_CACHE_TIMEOUT"]
        one_sec = timedelta(seconds=1)

        # cep is still valid
        CepCache.all_ceps.update(updated_at=timeout_limit - one_sec)
        with self.assertRaises(KeyError):
            _ = db_cache[sample_cep.cep]

        # cep is no longer valid
        CepCache.all_ceps.update(updated_at=timeout_limit + one_sec)
        self.assertIsNotNone(db_cache[sample_cep.cep])
