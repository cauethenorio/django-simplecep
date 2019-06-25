from django.test import TestCase
from django.forms import Form

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
        class SimpleForm(Form):
            cep = CEPField()

        form = SimpleForm()
        self.assertIn('maxlength="9"', form.as_p())

        class AnotherSimpleForm(Form):
            cep = CEPField(max_length=12)

        form = AnotherSimpleForm()
        self.assertIn('maxlength="12"', form.as_p())
