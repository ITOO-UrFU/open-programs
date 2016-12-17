clean:
	rm -f db.sqlite3

addroot:
	python manage.py addroot root

db:
	python manage.py makemigrations --noinput
	python manage.py migrate --noinput

server:
	python manage.py runserver

watch:
	cd constructor && $(MAKE) watch

setup:
	cd constructor && $(MAKE) setup

serve:
	cd constructor && $(MAKE) serve


backend: db server

frontend: watch serve

all: db server setup watch serve