"""Development settings."""
from .base import *  # noqa
from .base import env


# Allow to use weak passwords for development
AUTH_PASSWORD_VALIDATORS = []


# django-debug-toolbar
# https://django-debug-toolbar.readthedocs.io
# --------------------------------------------------------------------------
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
INSTALLED_APPS += ["debug_toolbar"]
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
