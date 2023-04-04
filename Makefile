server.dev:
	./manage.py runserver

server.dev.plus:
	./manage.py runserver_plus --cert-file cert.crt

makemigrations:
	./manage.py makemigrations

migrate:
	./manage.py migrate

compose.up:
	docker-compose -f docker-compose.dev.yml up --build

compose.down:
	docker-compose -f docker-compose.dev.yml down

dump_file_name = "mysite_data.json"

dump:
	./manage.py dumpdata --indent=2 --output=${dump_file_name}

# before loading the dump execute delete_contenttypes
delete_contenttypes:
	./manage.py shell -c "\
	from django.contrib.contenttypes.models import ContentType; \
	ContentType.objects.all().delete();\
	"

dump.load:
	./manage.py loaddata ${dump_file_name}


createsuperuser:
	./manage.py createsuperuser

celery_app_name = "config.celery_app"

run.celeryworker:
	celery -A ${celery_app_name} worker -l info

run.celery.flower:
	celery -A ${celery_app_name} flower

install.secrets:  # https://github.com/awslabs/git-secrets
	git secrets --install