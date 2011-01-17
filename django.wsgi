import os
import sys
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

sys.path.append(os.getcwd())

os.environ['DJANGO_SETTINGS_MODULE'] = 'eci.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
