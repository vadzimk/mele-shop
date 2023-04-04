# import celery module in the init file of the module will load celery when Django starts

from .celery import app as celery_app
__all__ = ['celery_app']