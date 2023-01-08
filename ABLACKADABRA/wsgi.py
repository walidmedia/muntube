"""
WSGI config for ABLACKADABRA project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                'ABLACKADABRA')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ABLACKADABRA.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

"""os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ABLACKADABRA.settings')

application = get_wsgi_application()"""
