import os
from celery import Celery
from celery.schedules import crontab
from Dewu.settings import PARSE_PERIOD

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Dewu.settings")
app = Celery("Dewu")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'changeLink': {
        'task': 'API.tasks.change_link',
        'schedule': crontab(minute=1),
    },
    'parseSPUs': {
        'task': 'API.tasks.parse_spu_ids',
        'schedule': crontab(hour=PARSE_PERIOD),
    },
}
