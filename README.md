# Selfhost Example Service (External)

The following code is an example of how to design a basic REST service for use with the NODA Self-host solution.

## The purpose of this skeleton code

To teach a developer how to design an asynchronous REST API.

The requirement for asynchronous requests stems from the fact that some requests take a long time to execute. Therefore we can not simply execute the code and return the result once the code has finished running, as such a solution would block the client for far too long and likely result in a timeout.

Instead, we propose a two-phase solution where the initial request immediately returns a tracking token, which we can then use to check the state of the request.

[Request example][fig1]

## Dependencies

Luckily, the problem we face is not new, and others have already figured out how to solve it.

[Celery](https://github.com/celery/celery) is an open-source asynchronous task queue or job queue based on distributed message passing.

[Redis](https://github.com/redis/redis) (Remote Dictionary Server) is an in-memory data structure store, used as a distributed, in-memory key-value database, cache and message broker, with optional durability. 

[Flask](https://github.com/pallets/flask) is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries.

[Flask-HTTPAuth](https://github.com/miguelgrinberg/Flask-HTTPAuth) is a Flask extension that simplifies the use of HTTP authentication with Flask routes.

As always with Python dependencies, there are sub-dependencies for all of the above items. However, we will not list these here as the above items are the only ones we are directly interested in.


## Project structure

- `app`: Application source code.
    + `services`: Add/Remove/Edit the content here as needed for your project.
        * `sleep.py`: An example service.
    + `celery_utils.py`: Celery instance helper.
    + `celery_worker.py`: Source file for the worker.
    + `factory.py`: Server application factory. 
    + `routes.py`: Edit this file to add your routes.
- `docs`: Documentation.
- `README.md`: This file.
- `server.py`: Source file for the server.
- `server_config.yaml.example`: Example config file for the server.
- `worker_config.yaml.example`: Example config file for the worker.


## Setting up an environment

1. You are going to need a working Redis server. The easiest way is to deploy an instance using Docker.
    1. Install [Docker](https://docs.docker.com/engine/install) or [Docker Desktop](https://www.docker.com/products/docker-desktop) depending on your platform of choice.
    2. Start a Redis instance in Docker.
        
        ```
        $ docker run --name redis -p 6379:6379 -d redis 
        ```

        **NOTE:** This will run a simple Redis instance on your localhost. Because of the way Docker exposes ports, anyone can access the instance from your local network. So keep that in mind.
2. Choose a project path for your code.
3. Download and extract (into your chosen location) the skeleton code from [https://github.com/noda/selfhost-service-skeleton](https://github.com/noda/selfhost-service-skeleton).
4. Create a virtual environment (or equivalent) and install all dependencies.

    ```
    $ virtualenv --python python3 venv
    $ source venv/bin/activate
    (venv)$ pip install -r requirements.txt
    ```

5. Copy the example config file `server_config.yaml.example` to `server_config.yaml`. We need to add "user:password" combinations to this file;
    1. Open the file in a text editor.
    2. Open a terminal window and activate the virtual environment from your project directory.
    3. Start the Python interpreter and execute the following.
    
        ```python
        >>> from werkzeug.security import generate_password_hash, check_password_hash
        >>> generate_password_hash('mypassword')
        'pbkdf2:sha256:150000$N0g7VyeR$8d0d97543987903cb8b9444f18bf437a34280d17e7e6a8ec8556910b0ab5a01c'
        ```

        Replace `mypassword` with the password you want to use. The string you received from the execution of `generate_password_hash` is your password hash. Copy it.

    4. Edit `server_config.yaml` so that it follows the following structure;

        ```yaml
        httpauth:
            myuser: "pbkdf2:sha256:150000$N0g7VyeR$8d0d97543987903cb8b9444f18bf437a34280d17e7e6a8ec8556910b0ab5a01c"
        ```

        You can add as many users as you need.

6. Copy the example config file `worker_config.yaml.example` to `worker_config.yaml`.

7. In two separate terminals;

    ```
    (venv)$ python server.py
    ```

    and

    ```
    (venv)$ celery -A app.celery_worker.celery worker --loglevel=info --pool=solo
    ```


    The system should now be up and running.

8. In your browser, visit the URL [http://127.0.0.1:5000/sleep/10](http://127.0.0.1:5000/sleep/10). This action will trigger a 10-second task. Then, watch the output from the Celery Worker.

## Adding a new task

To create a new task, add a file to the `app/services` path, for example;

- `apps/services/my_service.py`
- `apps/services/forecaster.py`
- `apps/services/emails.py`

Take a look at `apps/services/sleep.py` for an example of the structure required.

Once you've written the code, there are two more files that you need to edit;

- `services/__init__.py`: Init file for the services module.
- `apps/routes.py`: URL routes exposed via HTTP.

Import the function(s) you've created from the `services/__init__.py` file to the scope of the `app/routes.py` file. Then in the `apps/routes.py` file, declare the endpoints you want for your tasks, along with any code required to parse the request into arguments that you can pass along to your function(s).

Once again, take a look at `apps/services/sleep.py` and `apps/routes.py` for details about how to do this.

## The Celery Worker

### The --pool option

You can choose between processes or threads using the --pool command-line argument. For example, use a gevent execution pool, spawning 100 green threads (you need to pip-install gevent):

```
# start celery worker with the gevent pool
$ celery -A app.celery_worker.celery worker --loglevel=info --pool=gevent --concurrency=100
```

Don’t worry too much about the details (why are threads green?). We will go into more details if you carry on reading. Celery supports four execution pool implementations:

- prefork
- solo
- eventlet
- gevent

The --pool command-line argument is optional. If not specified, Celery defaults to the prefork execution pool.


### Why we prefer solo for --pool

The solo pool is a bit of a unique execution pool. Although, strictly speaking, the solo pool is neither threaded nor process-based, it is not even a pool as it is always solo.

The solo pool runs inside the worker process. It runs inline, which means there is no bookkeeping overhead. This solution makes the solo worker fast. But it also blocks the worker while it executes tasks, which has some implications when remote-controlling workers.

Using solo ensures that only one task is executed at a time on a worker, making it easier to predict the maximum load and memory requirements. Allowing you to handle the pool behaviour to another layer, such as Kubernetes, where you can have multiple instances of the same container.


[fig1]: https://github.com/noda/selfhost-service-skeleton/blob/main/docs/assets/request_example.svg "Request example"
