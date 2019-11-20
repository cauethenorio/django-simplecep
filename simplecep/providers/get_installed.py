from typing import List, Type

from django.utils.module_loading import import_string
from django.core.exceptions import ImproperlyConfigured

from simplecep.conf import simplecep_settings
from simplecep.providers.base import BaseCEPProvider


def get_installed_providers():
    providers_ids = set()
    providers: List[BaseCEPProvider] = []

    for provider_path in simplecep_settings["PROVIDERS"]:
        CEPProvider: Type[BaseCEPProvider] = import_string(provider_path)
        provider = CEPProvider(simplecep_settings["PROVIDERS_TIMEOUT"])

        if not hasattr(provider, "provider_id"):
            raise ImproperlyConfigured(
                "The {} CEP provider is missing the provider_id propery".format(
                    provider_path
                )
            )
        if provider.provider_id in providers_ids:
            raise ImproperlyConfigured(
                "More than one provider was created using the same provider_id: {}".format(
                    provider.provider_id
                )
            )
        providers.append(provider)
        providers_ids.add(provider.provider_id)

    return providers
