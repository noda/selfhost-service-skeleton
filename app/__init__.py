from celery import Celery


def make_celery(app_name=__name__):
    redis_url = "redis://localhost:6379"
    return Celery(app_name, backend=redis_url, broker=redis_url)


celery = make_celery()
