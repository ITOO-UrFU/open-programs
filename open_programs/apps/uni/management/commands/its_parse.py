import time
import json
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create Django objects from raw&ugly UrFU data."
    requires_system_checks = True
    requires_migrations_checks = True

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        start_time = time.time()

        class bcolors:
            HEADER = '\033[95m'
            OKBLUE = '\033[94m'
            OKGREEN = '\033[92m'
            WARNING = '\033[93m'
            FAIL = '\033[91m'
            ENDC = '\033[0m'
            BOLD = '\033[1m'
            UNDERLINE = '\033[4m'


        pr_filename = 'uni_fixtures/programs.json'
        pr = json.load(pr_filename)
        print(f"{bcolors.OKBLUE}{len(pr)}{bcolors.ENDC}")

        print(f"{bcolors.BOLD}--- {time.time() - start_time} секунд ---{bcolors.ENDC}")
