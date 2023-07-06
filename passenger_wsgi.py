# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u1920570/data/www/jarma.ru/website')
sys.path.insert(1, '/var/www/u1920570/data/djangoenv/lib/python3.7/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'website.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
