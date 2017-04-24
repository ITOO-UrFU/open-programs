from bs4 import BeautifulSoup
import re
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


    def handle(self, *args, **options):
        try:
            oksos = []
            with open('uni_fixtures/specialities.json', encoding='utf-8') as specialities:
                specialities_json = json.load(specialities)
                for speciality in specialities:
                    oksos.append(speciality["okso"])
        except:
            raise FileNotFoundError
        print(oksos)

