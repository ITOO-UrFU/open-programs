clean:
	rm -f db.sqlite3

db:
	./manage.py makemigrations --noinput
	./manage.py migrate --noinput
	./manage.py addroot root

server:
	./manage.py runserver

all: clean create_database server