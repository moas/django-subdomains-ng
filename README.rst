django-subdomains-ng
====================

Subdomain-based URL routing and reversing for Django. This project is inspired
by `django-subdomains by Ted Kaemming <https://github.com/tkaemming/django-subdomains>`_.

Requirements
------------

Django 5.2 LTS or later and Python 3.10 or later. Use a Python version
supported by your Django release. Django 5.2 supports Python 3.10 through
3.14, with Python 3.14 support starting in Django 5.2.8.

Installation
------------

.. code-block:: bash

    python -m pip install django-subdomains-ng

The Python package is imported as ``subdomains``.

Configuration
-------------

Add ``subdomains`` to ``INSTALLED_APPS``.
Add ``subdomains.middleware.SubdomainURLRoutingMiddleware`` to ``MIDDLEWARE``
before ``django.middleware.common.CommonMiddleware`` if you use it, so
slash redirects from CommonMiddleware also carry ``Vary: Host``.

.. code-block:: python

    ALLOWED_HOSTS = [".example.com"]
    SUBDOMAIN_BASE_DOMAIN = "example.com"

    ROOT_URLCONF = "myproject.urls"
    SUBDOMAIN_URLCONFS = {
        None: "myproject.urls",
        "api": "myproject.api_urls",
    }

Set ``SUBDOMAIN_BASE_DOMAIN`` to a hostname such as ``example.com``.
Routing and URL generation both use this setting. Replace the example
URLconf paths with modules in your project.

To use Django Sites instead, omit ``SUBDOMAIN_BASE_DOMAIN``, add
``django.contrib.sites`` to ``INSTALLED_APPS``, run
``python manage.py migrate``, and set ``SITE_ID`` to the Site whose domain
you want to use.

The middleware sets ``request.subdomain`` and selects a URLconf from
``SUBDOMAIN_URLCONFS``. Valid subdomains without a mapping use
``ROOT_URLCONF``. Use ``subdomains.middleware.SubdomainMiddleware`` if you
only need ``request.subdomain``.

Reversing URLs
--------------

.. code-block:: python

    from subdomains.utils import reverse

    reverse("home", subdomain="api", scheme="https")
    # https://api.example.com/

.. code-block:: django

    {% load subdomainurls %}
    {% url 'home' subdomain='api' %}

If the tag omits the subdomain, it uses the request's subdomain when the
request is in the template context. Enable the
``django.template.context_processors.request`` context processor to make
the request available. Pass ``subdomain=''`` to target the base domain
explicitly.

Development and release
-----------------------

.. code-block:: bash

    python -m pip install -e .
    make test

Run ``make test-matrix`` with tox and the supported Python interpreters
installed. To build and validate the distributions for PyPI:

.. code-block:: bash

    python -m pip install build twine
    python -m build
    python -m twine check --strict dist/*
    python -m twine upload dist/*

Use a clean ``dist/`` directory before building a release. The upload
requires PyPI credentials with permission to publish the project.
