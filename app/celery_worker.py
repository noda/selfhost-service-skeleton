import os
import yaml

from app import celery
from app.factory import create_app
from app.celery_utils import init_celery

config_filename = os.environ.get("CONFIG_FILENAME", "config.yaml")
config_content = ""

with open(config_filename, "r") as fd:
    config_content = fd.read()

cfg = yaml.safe_load(config_content)
app = create_app(celery_config=cfg)
init_celery(celery, app)
