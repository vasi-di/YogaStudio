from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'YogaApp.settings')

app = Celery('YogaApp')

app.config_from_object('django.conf:settings', namespace='CELERY_')

app.conf.beat_schedule = {
    'delete-old-yoga-classes': {
        'task': 'YogaApp.common.tasks.delete_old_yoga_classes',
        'schedule': crontab(hour=0, minute=0),
    },
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
