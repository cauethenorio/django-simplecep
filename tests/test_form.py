from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, override_settings
from django import forms

from simplecep.fields import CEPField


class CEPFormTestCase(TestCase):
    def test_cep_field_validation(self):
        field = CEPField()
        not_found_message = field.error_messages["not_found"]
        invalid_format_message = field.error_messages["invalid_format"]

        self.assertFieldOutput(
            CEPField,
            {
                "18170000": "18170-000",
                "18170-000": "18170-000",
                " 01001000": "01001-000",
                "01001-000": "01001-000",
            },
            {
                "10aa122": [invalid_format_message],
                "a": [invalid_format_message],
                "0000000": [invalid_format_message],
                "000000-000": [invalid_format_message],
                "18170-0000": [invalid_format_message],
                "11111111": [not_found_message],
                "11111-111": [not_found_message],
                "12345-123": [not_found_message],
            },
        )

    def test_cep_field_maxlength_should_be_9_as_default(self):
        class SimpleForm(forms.Form):
            cep = CEPField()

        form = SimpleForm()
        self.assertIn('maxlength="9"', form["cep"].as_widget())

        class AnotherSimpleForm(forms.Form):
            cep = CEPField(max_length=12)

        form = AnotherSimpleForm()
        self.assertIn('maxlength="12"', form["cep"].as_widget())

    def test_cep_field_should_not_add_autocomplete_attrs_by_default(self):
        class SimpleForm(forms.Form):
            cep = CEPField()

        form = SimpleForm()
        self.assertNotIn('data-simplecep-autocomplete"', form["cep"].as_widget())

    def test_cep_field_autcomplete_should_fail_with_wrong_keys(self):
        class SimpleForm(forms.Form):
            cep = CEPField(autocomplete_fields={"states": "state"})

        with self.assertRaisesMessage(
            ImproperlyConfigured,
            "Invalid CEPField autocomplete_fields param field type(s): ['states']",
        ):
            form = SimpleForm()
            form["cep"].as_widget()

    def test_cep_field_autcomplete_should_fail_with_wrong_field_name(self):
        class SimpleForm(forms.Form):
            cep = CEPField(autocomplete_fields={"state": "eztado"})
            estado = forms.CharField()

        with self.assertRaisesMessage(
            ImproperlyConfigured,
            "CEPField autocomplete_fields field not found: 'eztado'. "
            "Valid form fields: ['estado']",
        ):
            form = SimpleForm()
            form["cep"].as_widget()

    @override_settings(ROOT_URLCONF="tests.empty_urls")
    def test_cep_field_autocomplete_should_fail_without_getcep_endpoint(self):
        class SimpleForm(forms.Form):
            cep = CEPField(autocomplete_fields={"state": "state"})
            state = forms.CharField()

        with self.assertRaisesMessage(
            ImproperlyConfigured,
            "CEPField autcomplete_fields used but no 'simplecep:get-cep' view found",
        ):
            form = SimpleForm()
            form["cep"].as_widget()

    def test_cep_field_empty_autocomplete_fields_should_create_attrs(self):
        class SimpleForm(forms.Form):
            cep = CEPField(autocomplete_fields={"state": "estado"})
            estado = forms.CharField()

        form = SimpleForm()
        field_html = form["cep"].as_widget()

        self.assertIn("data-simplecep-autocomplete", field_html)
        self.assertIn('data-simplecep-state-field-id="id_estado"', field_html)

    def test_cep_field_should_correctly_use_custom_fields_ids(self):
        custom_id = "my_custom_id"

        class SimpleForm(forms.Form):
            cep = CEPField(autocomplete_fields={"address": "endereco"})
            endereco = forms.CharField(widget=forms.TextInput(attrs={"id": custom_id}))

        form = SimpleForm()
        field_html = form["cep"].as_widget()

        self.assertIn("data-simplecep-autocomplete", field_html)
        self.assertIn(
            'data-simplecep-address-field-id="{}"'.format(custom_id), field_html
        )
