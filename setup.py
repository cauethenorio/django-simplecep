import os
from setuptools import setup

requirements = ["Django>=2"]

test_requirements = ["tox==3.14.6", "coverage==5.1"]

dev_requirements = test_requirements + [
    "mypy==0.770",
    "flake8-bugbear==20.1.4",
    "black==19.10b0",
]

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.md")).read()

setup(
    name="django-simplecep",
    version="0.1.0",
    description="Validate brazilian zipcode (CEP) and auto-populate address fields using Correios API data",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/cauethenorio/django-simplecep",
    author="Cauê Thenório",
    author_email="caue@thenorio.com.br",
    packages=["simplecep"],
    python_requires=">=3.6",
    install_requires=requirements,
    extras_require={"dev": dev_requirements, "test": test_requirements},
    keywords=["django", "cep", "correios", "brasil", "endereço"],
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "Framework :: Django",
        "Environment :: Web Environment",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
    ],
    zip_safe=False,
)

# https://setuptools.readthedocs.io/en/latest/setuptools.html#configuring-setup-using-setup-cfg-files
