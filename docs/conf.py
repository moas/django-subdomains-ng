import os
import sys

from django.conf import settings

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from subdomains import __version__

if not settings.configured:
    settings.configure()


extensions = ['sphinx.ext.autodoc']
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = ['_build']

project = 'django-subdomains-ng'
copyright = '2012, ted kaemming'
version = release = '.'.join(map(str, __version__))

htmlhelp_basename = 'django-subdomains-ngdoc'

latex_elements = {}
latex_documents = [
  ('index', 'django-subdomains-ng.tex', 'django-subdomains-ng Documentation',
   'ted kaemming', 'manual'),
]

man_pages = [
    ('index', 'django-subdomains-ng', 'django-subdomains-ng Documentation',
     ['ted kaemming'], 1)
]

texinfo_documents = [
  ('index', 'django-subdomains-ng', 'django-subdomains-ng Documentation',
   'ted kaemming', 'django-subdomains-ng', 'One line description of project.',
   'Miscellaneous'),
]

autodoc_member_order = 'bysource'
autodoc_default_options = {'members': True}
