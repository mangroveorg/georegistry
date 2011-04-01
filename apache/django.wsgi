import os
import sys

sys.path.append('/home/aviars/django-apps/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'georegistry.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

