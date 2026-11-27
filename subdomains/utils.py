import functools
from urllib.parse import urlunsplit

from django.conf import settings
from django.urls import reverse as django_reverse


def current_site_domain():
    from django.contrib.sites.models import Site

    return Site.objects.get_current().domain


get_domain = current_site_domain


def urljoin(domain, path=None, scheme=None):
    """
    Joins a domain, path and scheme part together, returning a full URL.

    :param domain: the domain, e.g. ``example.com``
    :param path: the path part of the URL, e.g. ``/example/``
    :param scheme: the scheme part of the URL
    :returns: a full URL
    """
    return urlunsplit((scheme or '', domain, path or '', '', ''))


def reverse(viewname, subdomain=None, scheme=None, args=None, kwargs=None,
        current_app=None, request=None):
    """
    Reverses a URL from the given parameters, in a similar fashion to
    `django.urls.reverse <https://docs.djangoproject.com/en/5.2/ref/urlresolvers/#reverse>`_.

    :param viewname: the name of URL
    :param subdomain: the subdomain to use for URL reversing
    :param scheme: the scheme to use when generating the full URL, defaults to
        the value of ``settings.DEFAULT_URL_SCHEME``
    :param args: positional arguments used for URL reversing
    :param kwargs: named arguments used for URL reversing
    :param current_app: hint for the currently executing application
    :param request: optional request used to return a path for the same origin
    """
    urlconf = getattr(settings, 'SUBDOMAIN_URLCONFS', {}).get(subdomain)
    if urlconf is None:
        urlconf = settings.ROOT_URLCONF
    if scheme is None:
        scheme = getattr(settings, 'DEFAULT_URL_SCHEME', 'http')

    domain = get_domain()
    if subdomain is not None:
        domain = f'{subdomain}.{domain}'

    path = django_reverse(viewname, urlconf=urlconf, args=args, kwargs=kwargs,
        current_app=current_app)

    if (
        request is not None
        and domain.lower() == request.get_host().lower()
        and scheme in ('', request.scheme)
    ):
        return path

    return urljoin(domain, path, scheme=scheme)


#: :func:`reverse` bound to insecure (non-HTTPS) URLs scheme
insecure_reverse = functools.partial(reverse, scheme='http')

#: :func:`reverse` bound to secure (HTTPS) URLs scheme
secure_reverse = functools.partial(reverse, scheme='https')

#: :func:`reverse` bound to be relative to the current scheme
relative_reverse = functools.partial(reverse, scheme='')
