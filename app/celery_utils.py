def init_celery(celery, app):
    celery.conf["broker_url"] = "redis://localhost:6379"
    celery.conf["result_backend"] = "redis://localhost:6379"
    celery.conf.update(app.config.get("celery", {}))
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
