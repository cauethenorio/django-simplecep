from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from simplecep import CEPAddress
from simplecep.conf import simplecep_settings


class ValidCepsManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                updated_at__gte=timezone.now() - simplecep_settings["CEP_CACHE_MAXAGE"]
            )
        )


class CepCache(models.Model):
    cep = models.CharField(_("CEP"), max_length=8, primary_key=True)
    state = models.CharField(_("State"), max_length=2, null=False)
    city = models.CharField(_("City"), max_length=128, null=False)
    district = models.CharField(_("District"), max_length=128, null=True)
    street = models.CharField(_("Address"), max_length=128, null=True)

    provider = models.CharField(_("Provider"), max_length=128)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True, db_index=True)

    valid_ceps = ValidCepsManager()
    all_ceps = models.Manager()

    @classmethod
    def update_from_cep_address(cls, cep_address: CEPAddress):
        cls.all_ceps.update_or_create(
            cep=cep_address.cep, defaults=cep_address.to_dict(with_provider=True)
        )

    def to_cep_address(self) -> CEPAddress:
        return CEPAddress(
            cep=self.cep,
            street=self.street,
            state=self.state,
            district=self.district,
            city=self.city,
            provider=self.provider,
        )
