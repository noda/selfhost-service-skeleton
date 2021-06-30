# Selfhost Example Service (External)

The follow code is an example of how to design a basic REST service for use with the NODA Self-host solution.


## Dependencies

- Flask
- Celery 5+
- Redis


## Running the server

> python server.py


## Running the worker

> celery -A app.celery_worker.celery worker --loglevel=info --pool=solo

