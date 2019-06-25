from django.urls import re_path

from .views import CEPView


app_name = "simplecep"

urlpatterns = [re_path("(?P<cep>[0-9]{8})/$", CEPView.as_view(), name="get-cep")]
