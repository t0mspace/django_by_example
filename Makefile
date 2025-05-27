.PHONY: py-manage

py-createsuperuser:
	docker-compose exec web python3 manage.py createsuperuser

py-migrate:
	docker-compose exec web python3 manage.py migrate

py-startapp-%:
	docker-compose exec web python3 manage.py startapp $*

py-mkmigrations-%:
	docker-compose exec web python3 manage.py makemigrations $*

py-startproject-%:
	docker-compose exec web django-admin startproject $*

py-start:
	 docker compose up -d

py-build-start:
	 docker compose up -d --build

py-start-tests:
	docker compose exec web python manage.py test