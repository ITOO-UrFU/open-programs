import json
import grequests

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

        class GetPrograms:
            pr_filename = 'uni_fixtures/programs.json'

            def __init__(self):
                oksos = []

                with open('uni_fixtures/specialities.json', encoding='utf-8') as specialities:
                    specialities_json = json.load(specialities)
                    for speciality in specialities_json:
                        oksos.append(speciality["okso"])
                oksos = list(set(oksos))
                oksos = ["38.03.02", ]
                print("Всего ОКСО: ", len(oksos))

                open(self.pr_filename, 'w').close()
                self.urls = [f"http://its.urfu.ru/api/programs?okso={okso}" for okso in oksos]

            def exception(self, request, exception):
                print(f"Problem: {request.url}: {exception}")

            def async(self):
                results = grequests.map((grequests.get(u) for u in self.urls), exception_handler=self.exception, size=10)
                with open(self.pr_filename, 'a') as pr:
                    print("Загружаем программы из ИТС")
                    if results is not []:
                        print([r.content for r in results])
                        json.dump([r.content.decode('utf-8') for r in results], pr)
        get_programs = GetPrograms()
        get_programs.async()







