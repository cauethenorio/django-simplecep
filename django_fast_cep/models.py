from django.db import models
from django.utils.translation import gettext_lazy as _


class Cep(models.Model):
    cep = models.CharField(_("CEP"), max_length=8, primary_key=True)
    state = models.CharField(_("State"), max_length=2, null=False)
    city = models.CharField(_("City"), max_length=128, null=False)
    district = models.CharField(_("District"), max_length=128, null=True)
    address = models.CharField(_("Address"), max_length=128, null=True)
    number = models.CharField(_("Number"), max_length=64, null=True)
    extra = models.CharField(_("Extra"), max_length=128, null=True)
