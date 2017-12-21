"""
WSGI config for blogbootstrap project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
#from static_ranges import Ranges
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogbootstrap.settings")
application = get_wsgi_application()
#from whitenoise.django import DjangoWhiteNoise
#application = DjangoWhiteNoise(get_wsgi_application())


