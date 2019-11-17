from typing import List

from django.utils.module_loading import import_string
from django.core.exceptions import ImproperlyConfigured

from ..settings import SETTINGS
from .base import BaseCEPProvider  # noqa


def get_installed_providers():
    providers_ids = set()
    providers: List[BaseCEPProvider] = []

    for provider_path in SETTINGS["PROVIDERS"]:
        CEPProvider = import_string(provider_path)
        provider = CEPProvider()

        if not hasattr(provider, "provider_id"):
            raise ImproperlyConfigured(
                "The {} CEP provider is missing the id propery".format(provider_path)
            )
        if provider.provider_id in providers_ids:
            raise ImproperlyConfigured(
                "More than one provider was created using the same id: {}".format(
                    provider.id
                )
            )
        providers.append(provider)
        providers_ids.add(provider.provider_id)

    return providers
