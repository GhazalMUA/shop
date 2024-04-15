from celery import Celery
from datetime import timedelta
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE' , 'A.settings')
celery_app= Celery('A')
celery_app.autodiscover_tasks()

