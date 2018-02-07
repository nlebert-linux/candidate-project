from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# set up the default celery settings, coming from Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'birdview.settings')
app = Celery('birdview')

# Don't pickle objects
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# debug task that just dumps it's payload all over the console
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
