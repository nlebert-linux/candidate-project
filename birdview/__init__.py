from __future__ import absolute_import
# Always import the celery app when django starts
from .celery import app as celery_app
