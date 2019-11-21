import json
import re

from django import forms
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.translation import gettext_lazy as _

from simplecep import get_cep_data
from simplecep.providers import NoAvailableCepProviders


class CepFieldWidget(forms.TextInput):
    template_name = "simplecep/widgets/cep.html"

    def __init__(self, attrs=None, show_loading=True):
        self.show_loading = show_loading
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["show_loading"] = self.show_loading
        return context

    class Media:
        js = ("simplecep/simplecep-autofill.js",)


class CEPBoundField(forms.BoundField):
    valid_field_types = ("state", "city", "district", "address")

    @staticmethod
    def get_getcep_url():
        try:
            return reverse("simplecep:get-cep", kwargs={"cep": "00000000"})
        except NoReverseMatch:
            raise ImproperlyConfigured(
                "CEPField autofill used but no "
                "'simplecep:get-cep' view found. Include simplecep "
                "URLconf in your project urls.py"
            )

    def validate_and_get_fields(self):
        fields_keys = self.field.autofill_fields.keys()
        valid_field_types = self.valid_field_types

        invalid_fields = list(fields_keys - valid_field_types)
        if len(invalid_fields):
            raise ImproperlyConfigured(
                "Invalid CEPField autofill param field "
                "type(s): {}. Valid types: {}".format(invalid_fields, valid_field_types)
            )
        return self.field.autofill_fields

    def get_field_id(self, field_name: str) -> str:
        # DOM node IDs are allowed - no field lookup will be made
        if field_name[0] in ("#", "."):
            return field_name

        try:
            bound_field = self.form[field_name]
        except KeyError:
            raise ImproperlyConfigured(
                "CEPField autofill field not found: '{}'. "
                "Valid form fields: {}".format(
                    field_name, list(self.form.fields.keys() - [self.name])
                )
            )
        return "#{}".format(
            bound_field.field.widget.attrs.get("id") or bound_field.auto_id
        )

    def build_widget_attrs(self, attrs, widget=None):
        attrs = super().build_widget_attrs(attrs, widget)

        if self.field.autofill_fields is not None:
            fields = self.validate_and_get_fields()

            if len(fields.keys()):
                attrs["data-simplecep-autofill"] = json.dumps(
                    {
                        "baseCepURL": self.get_getcep_url(),
                        "dataFields": [
                            {
                                "type": field_type,
                                "selector": self.get_field_id(field_name),
                            }
                            for field_type, field_name in fields.items()
                        ],
                    },
                    sort_keys=True,
                )
        return attrs


class CEPField(forms.CharField):
    widget = CepFieldWidget

    default_error_messages = {
        "invalid_format": _("Invalid CEP format"),
        "not_found": _("CEP not found"),
        "no_available_providers": _("No available CEP providers at the moment"),
    }

    def __init__(self, *args, autofill=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.autofill_fields = autofill

    def validate_format(self, value: str) -> str:
        match = re.match(r"^(\d{5})-?(\d{3})$", value)
        if match is None:
            raise ValidationError(
                self.error_messages["invalid_format"], code="invalid_format"
            )
        return "".join(match.groups())

    def validate_exists(self, cep):
        try:
            cep = get_cep_data(cep)
            if not cep:
                raise ValidationError(
                    self.error_messages["not_found"], code="not_found"
                )
        except NoAvailableCepProviders:
            raise ValidationError(
                self.error_messages["no_available_providers"],
                code="no_available_providers",
            )
        # we use this data in get-cep view
        self.cep_data = cep

    def clean(self, value: str):
        value = super().clean(value)

        if value in self.empty_values:
            return value

        raw_cep = self.validate_format(value)
        self.validate_exists(raw_cep)
        return "{}-{}".format(raw_cep[:5], raw_cep[5:])

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)

        # set a max_length if it's not defined
        attrs.setdefault("maxlength", 9)

        # show numeric keyboard on mobile phones
        # https://css-tricks.com/everything-you-ever-wanted-to-know-about-inputmode/
        attrs["inputmode"] = "decimal"

        return attrs

    def get_bound_field(self, form, field_name):
        return CEPBoundField(form, self, field_name)
