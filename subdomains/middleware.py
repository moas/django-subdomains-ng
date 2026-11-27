import logging
import re

from django.conf import settings
from django.utils.cache import patch_vary_headers
from django.utils.deprecation import MiddlewareMixin

from subdomains.utils import get_domain

logger = logging.getLogger(__name__)


class SubdomainMiddleware(MiddlewareMixin):
    """
    A middleware class that adds a ``subdomain`` attribute to the request.
    """
    def get_domain_for_request(self, request):
        """
        Returns the domain that will be used to identify the subdomain part
        for this request.
        """
        return get_domain()

    def process_request(self, request):
        """
        Adds a ``subdomain`` attribute to the ``request`` parameter.
        """
        domain = self.get_domain_for_request(request).lower()
        host = request.get_host()

        if getattr(settings, 'REMOVE_WWW_FROM_DOMAIN', False):
            domain = domain.removeprefix('www.')

        pattern = rf'(?:(?P<subdomain>.*?)\.)?{re.escape(domain)}(?::[0-9]+)?'
        matches = re.fullmatch(pattern, host.lower())

        if matches:
            request.subdomain = matches.group('subdomain')
        else:
            request.subdomain = None
            logger.warning('The host %s does not belong to the domain %s, '
                'unable to identify the subdomain for this request',
                host, domain)


class SubdomainURLRoutingMiddleware(SubdomainMiddleware):
    """
    A middleware class that allows for subdomain-based URL routing.
    """
    def process_request(self, request):
        """
        Sets the current request's ``urlconf`` attribute to the urlconf
        associated with the subdomain, if it is listed in
        ``settings.SUBDOMAIN_URLCONFS``.
        """
        super().process_request(request)

        subdomain = request.subdomain
        urlconf = getattr(settings, 'SUBDOMAIN_URLCONFS', {}).get(subdomain)
        if urlconf is not None:
            logger.debug("Using urlconf %r for subdomain: %r", urlconf, subdomain)
            request.urlconf = urlconf

    def process_response(self, request, response):
        """
        Adds the HTTP ``Vary`` header to responses to avoid having responses
        cached across subdomains.
        """
        if getattr(settings, 'FORCE_VARY_ON_HOST', True):
            patch_vary_headers(response, ('Host',))

        return response
