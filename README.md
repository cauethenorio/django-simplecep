# django-simplecep

Django-simplecep helps you to fetch Brazilian address data associated to a CEP
value. It also auto-populates form address-fields based on provided CEP.

Example:
[image] 

## How it works

The library uses the configured data providers to fetch the CEP data.
Each installed provider is used until the data is successfully fetched.

By default it will use as data-provider, in order:
  1. Official Correios API (SIGEP WEB)
  2. www.republicavirtual.com.br API
  3. viacep.com.br API
  
After fetch, the retrieved data is cached (by default on a Django model)
so any data-retrieval attempt for the same CEP is resolved much faster and
do not use external providers.

The providers and the cache mechanism can be fully customized by the user.

If the CEP data isn't cached and all providers fail,
the `NoAvailableCepProviders` exception is raised.

## Usage

This library can be used in three different ways:

### As Python function

```python
>>> from simplecep.fetcher import get_cep_data
>>> cep_data = get_cep_data('59615350')

>>> cep_data
<CEPAddress 59615350>

>>> cep_data.to_dict()
{'cep': '59615350', 'street': 'Rua João Simão do Nascimento', 'state': 'RN', 'district': 'Santa Delmira', 'city': 'Mossoró'}
```

### As Django app API endpoint

You can include the `simplecep` URLconf into your Django project URLs to be
able to query CEP data using HTTP requests:

```shell
curl "http://localhost:8000/cep/59615350/"
{"cep": "59615350", "street": "Rua João Simão do Nascimento", "state": "RN", "district": "Santa Delmira", "city": "Mossoró"}
``` 

### As Django form field

The library provides the `CepField` form field which auto-populate other
address fields in the form when a CEP is typed by the user.

```python
from simplecep import CEPField

class CepForm(forms.Form):
    cep = CEPField(
        label='Your CEP',
        autofill={
            # key is the data-type and value is the form-field name
            "district": "bairro",
            "state": "estado",
            "city": "cidade",
            "street": "rua",
            "street_number": "numbero_rua",
        }
    )
    estado = forms.CharField()
    cidade = forms.CharField()
    bairro = forms.CharField()
    rua = forms.CharField()
    numbero_rua = forms.CharField()
```

The `CepField` form field uses Javascript (no jquery) to retrieve the data
from the CEP endpoint available on your app. It can be totally customized.

## Installation

1. Install the `django-simplecep` package using `pip` or your favourite python
package-manager:

   ```shell
   pip install django-cep
    ```

2. Adds `simplecep` to your Django `INSTALLED_APPS` setting:

    ```python
       INSTALLED_APPS = (
           # your other installed apps here
           # ...
           'simplecep',
       )
    ```
   
3. Run Django `migrate` command to create the CEP cache table:

   ```shell
   python manage.py migrate
    ```

4. Include the `simplecep` URLconf in your project `urls.py`:

    ```python
   urlpatterns = [
       # your app paths here
       path('cep/', include('simplecep.urls')),
   ]
    ```
   
   This step is optional and can be skipped if you won't use the CEP API
   endpoint or the `CepField` form field.

## Configuration

The library tries to use sane default-values, so you can use it without any additional
configuration, but you can configure it adding a `SIMPLECEP` object to your
Django settings file.

Here's the default configuration:

```python
SIMPLECEP = {
    # a list of CEP providers modules - you can create your own
    "PROVIDERS": (
        "simplecep.providers.CorreiosSIGEPCEPProvider",
        "simplecep.providers.RepublicaVirtualCEPProvider",
        "simplecep.providers.ViaCEPProvider",
    ),
    # the cache class - it should implement dict methods
    "CACHE": "simplecep.cache.CepDatabaseCache",
    # max-time to wait for each provider response in secs
    "PROVIDERS_TIMEOUT": 2,
    # time to keep the cached data - 6 months by default
    "CEP_CACHE_MAXAGE": datetime.timedelta(days=30 * 6),
}
```
## Customizing the CepField JS behaviour

By default the Javascript code included by the `CepField`:
- Adds a mask to the CEP field so value format is always 99999-999
- Fetches the CEP data using the browser `fetch` function
- Shows a loading indicator in the CEP field while data is being fetched
- Makes address fields `readonly` while the data is being fetched
- Populate address fields with obtained CEP data
- Focus on the next not-populated address field after populating the fields

Some behaviours above can be customized using `CepField` parameters.
All behaviours can be customized writing some JS code.

## Requirements

* Django 2.0 or higher
* Python 3.6 or higher 
