import os

from celery import (
    Celery,
)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'markets_bridge.settings')

app = Celery('markets_bridge')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
