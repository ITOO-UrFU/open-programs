import json
import grequests
import time

from django.core.management.base import BaseCommand

from programs.models import Program, ProgramModules, LearningPlan
from disciplines.models import Discipline, Semester, TrainingTerms
from modules.models import Module


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
                    for speciality in specialities_json:
                        oksos.append(speciality["okso"])
                oksos = list(set(oksos))
                print(f"{bcolors.OKGREEN}Всего ОКСО: {len(oksos)}{bcolors.ENDC}")

                open(self.pr_filename, 'w').close()
                self.urls = [f"http://its.urfu.ru/api/programs?okso={okso}" for okso in oksos]

            def exception(self, request, exception):
                print(f"Problem: {request.url}: {exception}")

            def async(self):
                results = grequests.map((grequests.get(u) for u in self.urls), exception_handler=self.exception, size=10)
                with open(self.pr_filename, 'a') as pr:
                    print(f"{bcolors.OKGREEN}Загружаем программы из ИТС{bcolors.ENDC}")
                    data = []
                    for r in results:
                        for i in r.json():
                            data.append(i)
                    json.dump(data, pr)

        get_programs = GetPrograms()
        get_programs.async()
        print(f"{bcolors.BOLD}--- {time.time() - start_time} секунд ---{bcolors.ENDC}")







