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

    programs = []
    oksos = []

    def handle(self, *args, **options):
        try:
            with open('uni_fixtures/specialities.json', encoding='utf-8') as specialities:
                specialities_json = json.load(specialities)
                for speciality in specialities_json:
                    self.oksos.append(speciality["okso"])
        except:
            raise FileNotFoundError
        for okso in oksos:
            r = requests.get(f"http://its.urfu.ru/api/programs?okso={okso}")
            self.programs.append(r.json())

        with open('uni_fixtures/programs.json', 'w') as pr:
            json.dump(self.programs, pr)

