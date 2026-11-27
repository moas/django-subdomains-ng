SECRET_KEY = "django-subdomains-ng-tests"
ALLOWED_HOSTS = [".example.com"]
INSTALLED_APPS = ["django.contrib.sites", "subdomains"]
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
SITE_ID = 1
ROOT_URLCONF = "subdomains.tests.urls.application"
MIDDLEWARE = [
    "subdomains.middleware.SubdomainURLRoutingMiddleware",
    "django.middleware.common.CommonMiddleware",
]
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates", "APP_DIRS": True}]
SUBDOMAIN_URLCONFS = {
    None: "subdomains.tests.urls.marketing",
    "api": "subdomains.tests.urls.api",
    "www": "subdomains.tests.urls.marketing",
}
