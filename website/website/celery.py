from __future__ import absolute_import, unicode_literals
import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
celery_application = Celery("website")
celery_application.config_from_object("django.conf:settings", namespace="CELERY")
celery_application.conf.broker_url = "amqp://rabbit:5672"
celery_application.autodiscover_tasks()