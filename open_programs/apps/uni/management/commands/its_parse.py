import requests
import json

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
    pr_filename = 'uni_fixtures/programs.json'
    oksos = []

    def handle(self, *args, **options):
        try:
            with open('uni_fixtures/specialities.json', encoding='utf-8') as specialities:
                specialities_json = json.load(specialities)
                for speciality in specialities_json:
                    self.oksos.append(speciality["okso"])
            self.oksos = list(set(self.oksos))
            print("Всего ОКСО:", len(self.oksos))
        except:
            raise FileNotFoundError
        open(self.pr_filename, 'w').close()
        with open(self.pr_filename, 'a') as pr:
            print("Загружаем программы из ИТС")
            for okso in self.oksos:
                r = requests.get(f"http://its.urfu.ru/api/programs?okso={okso}")
                print(okso, "status: ", r.status_code, "length: ", len(r.json()))
                if r.json() is not []:
                    json.dump(r.json(), pr)




