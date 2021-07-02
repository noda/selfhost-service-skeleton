import os
import yaml

from app import factory
import app

if __name__ == "__main__":
    config_filename = os.environ.get("CONFIG_FILENAME", "server_config.yaml")
    config_content = ""

    with open(config_filename, "r") as fd:
       config_content = fd.read()

    cfg = yaml.safe_load(config_content)
    app = factory.create_app(celery=app.celery, config=cfg)
    app.run()
