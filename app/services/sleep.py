import time

from app import celery

@celery.task(name="services.sleep")
def sleep(_time, name):
    time.sleep(_time)
    return name
