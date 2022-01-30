from app import celery


@celery.task(name="maths.add")
def add(a, b):
    return a + b


@celery.task(name="maths.sub")
def sub(a, b):
    return a - b


@celery.task(name="maths.mul")
def mul(a, b):
    return a * b


@celery.task(name="maths.div")
def div(a, b):
    return a / b


@celery.task(name="maths.mod")
def mod(a, b):
    return a % b
