import re

from django import forms
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.translation import gettext_lazy as _

from simplecep.models import Cep


def with_prefix(field: str) -> str:
    return "data-simplecep-{}".format(field)


class CEPBoundField(forms.BoundField):
    valid_field_types = ("state", "city", "district", "address")

    @staticmethod
    def get_getcep_url():
        try:
            return reverse("simplecep:get-cep", kwargs={"cep": "00000000"})
        except NoReverseMatch:
            raise ImproperlyConfigured(
                "CEPField autcomplete_fields used but no "
                "'simplecep:get-cep' view found. Include simplecep "
                "URLconf in your project urls.py"
            )

    def validate_and_get_fields(self):
        fields_keys = self.field.autocomplete_fields.keys()
        valid_field_types = self.valid_field_types

        invalid_fields = list(fields_keys - valid_field_types)
        if len(invalid_fields):
            raise ImproperlyConfigured(
                "Invalid CEPField autocomplete_fields param field "
                "type(s): {}. Valid types: {}".format(invalid_fields, valid_field_types)
            )
        return self.field.autocomplete_fields

    def get_field_id(self, field_name: str) -> str:
        # DOM node IDs are allowed - no field lookup will be made
        if field_name.startswith("#"):
            return field_name

        try:
            bound_field = self.form[field_name]
        except KeyError:
            raise ImproperlyConfigured(
                "CEPField autocomplete_fields field not found: '{}'. "
                "Valid form fields: {}".format(
                    field_name, list(self.form.fields.keys() - [self.name])
                )
            )
        return bound_field.field.widget.attrs.get("id") or bound_field.auto_id

    def build_widget_attrs(self, attrs, widget=None):
        attrs = super().build_widget_attrs(attrs, widget)

        if self.field.autocomplete_fields is not None:
            fields = self.validate_and_get_fields()

            if len(fields.keys()):
                # tell JS this field is an CEP autocomplete source
                attrs[with_prefix("autocomplete")] = True
                attrs[with_prefix("get-cep-url")] = self.get_getcep_url()

                for field_type, field_name in fields.items():
                    attr_key = with_prefix("{}-field-id").format(field_type)
                    attrs[attr_key] = self.get_field_id(field_name)

        return attrs


class CEPField(forms.CharField):
    default_error_messages = {
        "invalid_format": _("Invalid CEP format"),
        "not_found": _("CEP not found"),
    }

    def __init__(self, *args, autocomplete_fields=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.autocomplete_fields = autocomplete_fields

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

        # set a max_length if it's not defined
        attrs.setdefault("maxlength", 9)

        # show numeric keyboard on mobile phones
        # https://css-tricks.com/everything-you-ever-wanted-to-know-about-inputmode/
        attrs["inputmode"] = "decimal"

        return attrs

    def get_bound_field(self, form, field_name):
        return CEPBoundField(form, self, field_name)
