clean:
	rm -f db.sqlite3

db:
	./manage.py makemigrations --noinput
	./manage.py migrate --noinput
	-./manage.py addroot root

server:
	./manage.py runserver

watch:
	cd constructor && $(MAKE) watch

setup:
	cd constructor && $(MAKE) setup

serve:
	cd constructor && $(MAKE) serve

all: db server setup watch serve

backend: server

frontend: setup watch serve
