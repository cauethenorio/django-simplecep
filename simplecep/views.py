from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import View


from simplecep import CEPField


class CEPView(View):
    errors_statuses = {
        "invalid_format": 400,
        "not_found": 404,
        "no_available_providers": 500,
    }

    def get(self, request, *args, cep=None):
        cep_field = CEPField()
        try:
            cep_field.clean(cep)
        except ValidationError as e:
            return JsonResponse(
                {"error": e.code, "message": e.message},
                status=self.errors_statuses[e.code],
            )

        cep_data = cep_field.cep_data
        return JsonResponse(cep_data.to_dict())
