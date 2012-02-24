import os
from os.path import dirname, abspath, join

_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
activate_this = os.path.join(_PROJECT_ROOT, "ve/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

os.environ['DJANGO_SETTINGS_MODULE'] = 'powwow.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
