from django.db import models
from django.utils.translation import gettext_lazy as _


class CachedCep(models.Model):
    cep = models.CharField(_("CEP"), max_length=8, primary_key=True)
    state = models.CharField(_("State"), max_length=2, null=False)
    city = models.CharField(_("City"), max_length=128, null=False)
    neighborhood = models.CharField(_("Neighborhood"), max_length=128, null=True)
    street = models.CharField(_("Address"), max_length=128, null=True)

    provider = models.CharField(_("Provider"), max_length=128)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
