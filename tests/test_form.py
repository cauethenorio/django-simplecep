import html
import json
from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, override_settings
from django import forms

from simplecep import CEPField, NoAvailableCepProviders


def html_decode(html_fragment) -> str:
    return html.escape(json.dumps(html_fragment, sort_keys=True))


@patch("simplecep.fields.get_cep_data")
class CEPFormTestCase(TestCase):
    def test_cep_field_format_validation(self, *args):
        invalid_format_message = CEPField.default_error_messages["invalid_format"]

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
            },
        )

    def test_cep_field_cep_not_found_validation(self, mocked_get_cep_data):
        not_found_message = CEPField.default_error_messages["not_found"]
        mocked_get_cep_data.return_value = None
        self.assertFieldOutput(
            CEPField,
            {},
            {
                "11111111": [not_found_message],
                "11111-111": [not_found_message],
                "12345-123": [not_found_message],
            },
        )

    def test_cep_field_cep_found_validation(self, mocked_get_cep_data):
        # The real function will return a CEPAdress instance
        # but the fields only checks if it's null
        mocked_get_cep_data.return_value = True
        self.assertFieldOutput(
            CEPField,
            {
                "11111111": "11111-111",
                "11111-111": "11111-111",
                "12345-123": "12345-123",
            },
            {},
        )

    def test_cep_field_no_available_providers_validation(self, mocked_get_cep_data):
        no_providers_message = CEPField.default_error_messages["no_available_providers"]
        mocked_get_cep_data.side_effect = NoAvailableCepProviders()
        self.assertFieldOutput(CEPField, {}, {"11111111": [no_providers_message]})

    def test_cep_field_maxlength_should_be_9_as_default(self, *args):
        class SimpleForm(forms.Form):
            cep = CEPField()

        form = SimpleForm()
        self.assertIn('maxlength="9"', form["cep"].as_widget())

        class AnotherSimpleForm(forms.Form):
            cep = CEPField(max_length=12)

        form = AnotherSimpleForm()
        self.assertIn('maxlength="12"', form["cep"].as_widget())

    def test_cep_field_should_not_add_autofill_attrs_by_default(self, *args):
        class SimpleForm(forms.Form):
            cep = CEPField()

        form = SimpleForm()
        self.assertNotIn('data-simplecep-autofill"', form["cep"].as_widget())

    def test_cep_autofill_should_fail_with_wrong_keys(self, *args):
        class SimpleForm(forms.Form):
            cep = CEPField(autofill={"states": "state"})

        with self.assertRaisesMessage(
            ImproperlyConfigured,
            "Invalid CEPField autofill param field type(s): ['states']",
        ):
            form = SimpleForm()
            form["cep"].as_widget()

    def test_cep_autofill_should_fail_with_wrong_field_name(self, *args):
        class SimpleForm(forms.Form):
            cep = CEPField(autofill={"state": "eztado"})
            estado = forms.CharField()

        with self.assertRaisesMessage(
            ImproperlyConfigured,
            "CEPField autofill field not found: 'eztado'. "
            "Valid form fields: ['estado']",
        ):
            form = SimpleForm()
            form["cep"].as_widget()

    @override_settings(ROOT_URLCONF="tests.empty_urls")
    def test_cep_field_autofill_should_fail_without_getcep_endpoint(self, *args):
        class SimpleForm(forms.Form):
            cep = CEPField(autofill={"state": "state"})
            state = forms.CharField()

        with self.assertRaisesMessage(
            ImproperlyConfigured,
            "CEPField autofill used but no 'simplecep:get-cep' view found",
        ):
            form = SimpleForm()
            form["cep"].as_widget()

    def test_cep_field_autofill_should_send_baseurl(self, *args):
        class SimpleForm(forms.Form):
            cep = CEPField(autofill={"city": "#cidade"})

        form = SimpleForm()
        field_html = form["cep"].as_widget()
        self.assertIn(html.escape('"baseCepURL": "/cep/00000000/"'), field_html)

    def test_cep_field_empty_autofill_should_create_attrs(self, *args):
        class SimpleForm(forms.Form):
            cep = CEPField(autofill={"district": "bairro_xyz"})
            bairro_xyz = forms.CharField()

        form = SimpleForm()
        field_html = form["cep"].as_widget()

        self.assertIn("data-simplecep-autofill=", field_html)
        self.assertIn(
            html_decode(
                [{"type": "district", "selector": "#" + form["bairro_xyz"].auto_id}]
            ),
            field_html,
        )

    def test_cep_field_should_correctly_use_custom_fields_ids(self, *args):
        custom_id = "my_custom_id"

        class SimpleForm(forms.Form):
            cep = CEPField(autofill={"address": "endereco"})
            endereco = forms.CharField(widget=forms.TextInput(attrs={"id": custom_id}))

        form = SimpleForm()
        field_html = form["cep"].as_widget()

        self.assertIn("data-simplecep-autofill", field_html)
        self.assertIn(
            html_decode([{"type": "address", "selector": "#" + custom_id}]), field_html
        )

    def test_cep_field_empty_autofill_with_id_should_not_lookup_fields(self, *args):
        class SimpleForm(forms.Form):
            cep = CEPField(autofill={"state": "#some_node_id", "district": ".bairro"})

        form = SimpleForm()
        field_html = form["cep"].as_widget()

        self.assertIn("data-simplecep-autofill", field_html)
        self.assertIn(
            html_decode({"type": "district", "selector": ".bairro"}), field_html
        )
        self.assertIn(
            html_decode({"type": "state", "selector": "#some_node_id"}), field_html
        )
