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
            def __init__(self):
                pr_filename = 'uni_fixtures/programs.json'
                oksos = []
                try:
                    with open('uni_fixtures/specialities.json', encoding='utf-8') as specialities:
                        specialities_json = json.load(specialities)
                        for speciality in specialities_json:
                            self.oksos.append(speciality["okso"])
                    self.oksos = list(set(self.oksos))
                    print("Всего ОКСО: ", len(self.oksos))
                except:
                    raise FileNotFoundError
                open(pr_filename, 'w').close()
                self.urls = [f"http://its.urfu.ru/api/programs?okso={okso}" for okso in oksos]

            def exception(self, request, exception):
                print(f"Problem: {request.url}: {exception}")

            def async(self):
                results = grequests.map((grequests.get(u) for u in self.urls), exception_handler=self.exception, size=5)
                with open(self.pr_filename, 'a') as pr:
                    print("Загружаем программы из ИТС")
                    if results.json() is not []:
                        json.dump(results.json(), pr)
        get_programs = GetPrograms()
        get_programs.async()







