from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='+', type=str)

    def handle(self, *args, **options):
        for username in options['username']:
            User.objects.create_superuser(username, username + '@example.com', '123')
            self.stdout.write(self.style.SUCCESS('Add superuser "%s", password: 123' % username))