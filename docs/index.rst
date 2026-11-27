django-subdomains-ng
====================

Subdomain helpers for the Django framework, including subdomain-based URL
routing and reversing.

Installation
------------

Install from PyPI::

    python -m pip install django-subdomains-ng

Django 5.2 LTS or later and Python 3.10 or later are required. Use a
Python version supported by your Django release.

Quick Start
-----------

To set up subdomain URL routing and reversing in a Django project:

1. Add ``subdomains`` to ``INSTALLED_APPS``.
2. Add :class:`subdomains.middleware.SubdomainURLRoutingMiddleware` to
   ``MIDDLEWARE``. Place it before
   `CommonMiddleware <https://docs.djangoproject.com/en/5.2/ref/middleware/#django.middleware.common.CommonMiddleware>`_ so the routing
   middleware also adds ``Vary: Host`` to slash redirects.
3. Configure ``ALLOWED_HOSTS`` and ``SUBDOMAIN_URLCONFS``.
4. Set ``SUBDOMAIN_BASE_DOMAIN`` to the base hostname used for routing and
   URL generation. To use Django Sites instead, omit the setting, add
   ``django.contrib.sites`` to ``INSTALLED_APPS``, run migrations, and set
   ``SITE_ID`` to the Site with the desired domain.

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

::

    ALLOWED_HOSTS = ['.example.com']
    SUBDOMAIN_BASE_DOMAIN = 'example.com'

    # Unmapped subdomains use the project's root URLconf.
    ROOT_URLCONF = 'myproject.urls.account'

    # A dictionary of urlconf module paths, keyed by their subdomain.
    SUBDOMAIN_URLCONFS = {
        None: 'myproject.urls.frontend',  # no subdomain, e.g. ``example.com``
        'www': 'myproject.urls.frontend',
        'api': 'myproject.urls.api',
    }

Basic Usage
-----------

Using Subdomains in Views
~~~~~~~~~~~~~~~~~~~~~~~~~

On each request, a ``subdomain`` attribute will be added to the ``request``
object. You can use this attribute to select view behavior, like in this example::

    def user_profile(request):
        try:
            # Retrieve the user account associated with the current subdomain.
            user = User.objects.get(username=request.subdomain)
        except User.DoesNotExist:
            # No user matches the current subdomain, so return a generic 404.
            raise Http404

Resolving Named URLs by Subdomain
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Included is a :func:`subdomains.utils.reverse` function that responds similarly to
`django.urls.reverse <https://docs.djangoproject.com/en/5.2/ref/urlresolvers/#reverse>`_, but accepts optional ``subdomain``
and ``scheme`` arguments and does not allow a ``urlconf`` parameter.

If no ``subdomain`` argument is provided, the URL will be resolved relative to
the ``SUBDOMAIN_URLCONFS[None]`` or ``ROOT_URLCONF``, in order. The protocol
scheme is the value of ``settings.DEFAULT_URL_SCHEME``, or if unset, ``http``::

    >>> from subdomains.utils import reverse
    >>> reverse('home')
    'http://example.com/'
    >>> reverse('user-profile', kwargs={'username': 'ted'})
    'http://example.com/users/ted/'
    >>> reverse('home', scheme='https')
    'https://example.com/'

For subdomains, the URL will be resolved relative to the
``SUBDOMAIN_URLCONFS[subdomain]`` value if it exists, otherwise falling back to
the ``ROOT_URLCONF``::

    >>> from subdomains.utils import reverse
    >>> reverse('home', subdomain='api')
    'http://api.example.com/'
    >>> reverse('home', subdomain='wildcard')
    'http://wildcard.example.com/'
    >>> reverse('login', subdomain='wildcard')
    'http://wildcard.example.com/login/'

If a URL cannot be resolved, a ``django.urls.NoReverseMatch``
will be raised.

Resolving Named URLs in Templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``subdomainurls`` template tag library contains a ``url`` tag that takes an
optional ``subdomain`` argument as its first positional argument, or as named
argument. The following are all valid invocations of the tag::

    {% load subdomainurls %}
    {% url 'home' %}
    {% url 'home' 'subdomain' %}
    {% url 'home' subdomain='subdomain' %}
    {% url 'user-profile' username='ted' %}
    {% url 'user-profile' subdomain='subdomain' username='ted' %}

When the request is in the template context, the tag defaults to the
request's subdomain. Without a request, it defaults to the base domain.
Pass ``subdomain=''`` to select the base domain explicitly. Set
``django.template.context_processors.request`` in the Django template
engine's ``OPTIONS['context_processors']`` to make the request available.

API Reference
-------------

.. toctree::
   :maxdepth: 2
   :glob:

   ref/**

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

