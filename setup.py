import os
from setuptools import setup

requirements = [
    'Django>=2',
]

test_requirements = [
    "tox==3.12.1",
]

dev_requirements = test_requirements + [
    "mypy==0.701",
    "flake8-bugbear==19.3.0",
    "black==19.3b0",
]

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(
    name="django-fast-cep",
    version="0.1.0",
    description="Populated brazilian Correios CEP table into your django app",
    long_description=README,
    license="MIT",
    url="https://github.com/cauethenorio/django-fast-cep",
    author="Cauê Thenório",
    author_email="caue@thenorio.com.br",
    packages=["django_fast_cep"],
    python_requires=">=3.5",
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
        "test": test_requirements,
    },
    keywords=['django', 'cep', 'correios', 'brasil', 'endereço'],
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
    ],
    zip_safe=False,
)
