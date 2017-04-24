import os
import time
import json
import tempfile
import grequests
from shutil import copyfile

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

        class GetPrograms:
            pr_filename = 'uni_fixtures/programs.json'

            def __init__(self):
                oksos = []
                with open('uni_fixtures/specialities.json', encoding='utf-8') as specialities:
                    specialities_json = json.load(specialities)
                    [oksos.append(s["okso"]) for s in specialities_json]
                print(f"{bcolors.OKGREEN}Всего ОКСО: {len(list(set(oksos)))}{bcolors.ENDC}")
                self.urls = [f"http://its.urfu.ru/api/programs?okso={okso}" for okso in list(set(oksos))]

            def exception(self, request, exception):
                print(f"{bcolors.FAIL}Problem: {request.url}: {exception}{bcolors.ENDC}")

            def async(self):
                results = grequests.map((grequests.get(u) for u in self.urls), exception_handler=self.exception, size=100)
                with open(tempfile.TemporaryFile(), 'a') as pr:
                    print(f"{bcolors.OKGREEN}Загружаем программы из ИТС{bcolors.ENDC}")
                    data = []
                    [[data.append(i) for i in r.json() if len(i["variants"]) > 0] for r in results]
                    json.dump(data, pr)
                    if os.path.exists(pr):
                        copyfile(pr, self.pr_filename)

        get_programs = GetPrograms()
        get_programs.async()
        print(f"{bcolors.BOLD}--- {time.time() - start_time} секунд ---{bcolors.ENDC}")
