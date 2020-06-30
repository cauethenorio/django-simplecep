from django.shortcuts import render
from django.views.generic.edit import FormView

from .forms import CepForm


class CepFormView(FormView):
    template_name = "cep-form.html"
    form_class = CepForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form2"] = CepForm(prefix="2")
        return context
