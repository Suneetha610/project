"""
WSGI config for expenses project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
from django.core.wsgi import get_wsgi_application

# ✅ Correct settings module path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.expenses.settings')

application = get_wsgi_application()
