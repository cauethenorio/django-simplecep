import re

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from simplecep.models import Cep


class CEPField(forms.CharField):
    default_error_messages = {
        "invalid_format": _("Invalid CEP format"),
        "not_found": _("CEP not found"),
    }

    def validate_format(self, value: str) -> str:
        match = re.match("^(\\d{5})-?(\\d{3})$", value)
        if match is None:
            raise ValidationError(
                self.error_messages["invalid_format"], code="invalid_format"
            )
        return "".join(match.groups())

    def validate_exists(self, cep):
        if not Cep.objects.filter(pk=cep).exists():
            raise ValidationError(self.error_messages["not_found"], code="not_found")

    def clean(self, value: str):
        value = super().clean(value)

        if value in self.empty_values:
            return value

        raw_cep = self.validate_format(value)
        self.validate_exists(raw_cep)
        return "{}-{}".format(raw_cep[:5], raw_cep[5:])

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)

        # show numeric keyboard on mobile phones
        # https://css-tricks.com/everything-you-ever-wanted-to-know-about-inputmode/
        attrs["inputmode"] = "decimal"

        return attrs
