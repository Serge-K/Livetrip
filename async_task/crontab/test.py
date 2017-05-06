from pyramid_celery import celery_app as app
from datetime import datetime

import logging
log = logging.getLogger(__name__)


@app.task
def print_date(*args, **kwargs):
    log.info("------------> {}".format(datetime.now()))
    print("------------> {}".format(datetime.now()))
