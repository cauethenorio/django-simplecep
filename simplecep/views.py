from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views import View


from .models import CachedCep
from .fetcher import fetch_from_providers


class CEPView(View):
    def get(self, request, *args, cep=None):
        try:
            cep = CachedCep.valid_ceps.get(cep=cep)
            return JsonResponse(model_to_dict(cep))
        except CachedCep.DoesNotExist:
            return JsonResponse({"error": "cep_not_found"}, status=404)
