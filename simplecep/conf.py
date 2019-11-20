import datetime

from django.conf import settings


DEFAULT_SETTINGS = {
    "PROVIDERS": (
        "simplecep.providers.CorreiosSIGEPCEPProvider",
        "simplecep.providers.RepublicaVirtualCEPProvider",
        "simplecep.providers.ViaCEPProvider",
    ),
    "CACHE": "simplecep.cache.CepDatabaseCache",
    "PROVIDERS_TIMEOUT": 2,
    "CEP_CACHE_TIMEOUT": datetime.timedelta(days=30 * 6),
}


def get_merged_settings():
    """
    Merge default settings into default simple-cep settings
    """
    merged = DEFAULT_SETTINGS.copy()
    merged.update(getattr(settings, "SIMPLECEP", {}))
    return merged


simplecep_settings = get_merged_settings()
