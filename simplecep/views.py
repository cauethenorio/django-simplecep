from django.http import JsonResponse
from django.views import View


from simplecep import get_cep_data, NoCepProviderAvailable


class CEPView(View):
    def get(self, request, *args, cep=None):
        try:
            cep = get_cep_data(cep)
            if cep:
                return JsonResponse(cep.to_dict())
            return JsonResponse({"error": "cep_not_found"}, status=404)
        except NoCepProviderAvailable:
            return JsonResponse({"error": "no_cep_provider_available"}, status=500)
