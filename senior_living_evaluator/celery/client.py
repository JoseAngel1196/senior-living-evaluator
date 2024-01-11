from celery import Celery

from senior_living_evaluator.settings import CELERY_QUEUE_NAME

_CELERY_BROKER_URI = "redis://{CELERY_BROKER_ENDPOINT}/0"
_CELERY_RESULT_BACKEND_URI = "redis://{CELERY_BROKER_ENDPOINT}/1"


class CeleryBase:
    result_backend = _CELERY_RESULT_BACKEND_URI
    broker_url = _CELERY_BROKER_URI
    task_track_started = True
    timezone = "UTC"
    task_serializer = "json"
    result_serializer = "json"
    accept_content = ["json"]
    task_acks_late = True
    task_default_queue = CELERY_QUEUE_NAME
    broker_transport_options = {"visibility_timeout": 60}


celery_client = Celery("senior_living_evaluator")
celery_client.config_from_object(obj=CeleryBase)
