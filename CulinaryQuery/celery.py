from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

app = Celery('CulinaryQuery')

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

# Set timezone for Celery
app.conf.timezone = 'UTC'
