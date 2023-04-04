import os
from celery import Celery

# specify the DJANGO_SETTINGS_MODULE environment variable in your Celery configuration to tell Celery where to find the Django settings for your project.
#
# This is necessary because your Django project may have different settings for different environments, such as development, staging, and production. By specifying the DJANGO_SETTINGS_MODULE environment variable, you can ensure that Celery uses the correct settings for the environment in which it is running.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# myshop is the name of the Celery application that is being created using the Celery constructor. The name 'myshop' is arbitrary and can be changed to any other name you prefer.
app = Celery('myshop')  # celery application

#  specifies the settings module from the django.conf package.
#  By setting the CELERY namespace, all Celery settings need to include the CELERY_ preﬁx in their name (for example, CELERY_BROKER_URL).
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
