from django import forms

from simplecep import CEPField


class CepForm(forms.Form):
    cep = CEPField(
        autofill={
            "district": "district",
            "state": "state",
            "city": "city",
            "street": "street",
            "street_number": "street_number",
        }
    )
    state = forms.CharField()
    city = forms.CharField()
    district = forms.CharField()
    street = forms.CharField()
    street_number = forms.CharField()
