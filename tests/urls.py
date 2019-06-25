from django.urls import path, include

urlpatterns = [path("cep/", include("simplecep.urls"))]
