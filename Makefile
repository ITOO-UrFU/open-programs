clean:
	rm -f db.sqlite3

db:
	./manage.py makemigrations --noinput
	./manage.py migrate --noinput
	./manage.py addroot root

all: clean create_database