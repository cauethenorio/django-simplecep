from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views import View


from .models import Cep


class CEPView(View):
    def get(self, request, *args, cep=None):
        try:
            cep = Cep.objects.get(cep=cep)
            return JsonResponse(model_to_dict(cep))
        except Cep.DoesNotExist:
            return JsonResponse({"error": "cep_not_found"}, status=404)
