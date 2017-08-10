from bs4 import BeautifulSoup
import re
import json
import time

from django.core.management.base import BaseCommand

from programs.models import Program, ProgramModules, LearningPlan
from disciplines.models import Discipline, Semester, TrainingTerms
from modules.models import Module


class Command(BaseCommand):
    help = "Create Django objects from ITOO-UrFU/EPP-generated json."
    requires_system_checks = True
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('epp_json', nargs=1)
        parser.add_argument('program_title', nargs=1)

    def handle(self, *args, **options):
        epp_json = options["epp_json"][0]
        program_title = options["program_title"][0]

        with open(epp_json, encoding='utf-8') as epp_json:
            epp = json.loads('\n'.join(epp_json.readlines()))

        try:
            program = Program.objects.filter(title=program_title).first()
            program.status = "p"
            program.save()
        except:
            raise NotImplementedError

        stage = False if "stage" not in epp.keys() else True if "утверждено" in epp["stage"].lower() else False
        displayableTitle = None if "version" not in epp.keys() else epp["version"]
        number = None if "number" not in epp.keys() else epp["number"]
        active = None if "active" not in epp.keys() else epp["active"]
        title = None if "title" not in epp.keys() else epp["title"]

        term = None if "term" not in epp.keys() else epp["term"]

        lps = LearningPlan.objects.filter(uni_number=number, status="p")
        if len(lps) > 0:
            for lp in lps:
                lp.uni_displayableTitle = displayableTitle
                lp.uni_number = number
                lp.uni_active = active
                lp.uni_title = title
                lp.uni_stage = stage
                lp.uni_html = json.dumps(epp)
                lp.save()
                if lp not in program.learning_plans.all():
                    program.learning_plans.add(lp)
                    program.save()
        else:
            lp = LearningPlan(uni_displayableTitle=displayableTitle,
                              uni_number=number,
                              uni_active=active,
                              uni_title=title,
                              uni_stage=stage,
                              uni_html=json.dumps(epp),
                              status="p"
                              )
            lp.save()
            print(lp.id)
            program.learning_plans.add(lp)
            program.save()

            # Добавили учебный план

        if term == 8:
            term = TrainingTerms.objects.filter(title="4 года").first()
            for epp_module in epp["modules"]:
                module_obj, semester = self.create_module(epp_module, program)
                print(module_obj)

    def create_module(self, module, program):
        semester = min([int(d["firstSemester"]) for d in module["disciplines"]])
        module_obj = Module.objects.filter(uni_number=module["title"]).first()
        if module_obj:
            module_obj.uni_uuid = module["uuid"]
            module_obj.uni_number = module["number"]
            module_obj.uni_coordinator = module["coordinator"]
            module_obj.uni_type = module["type"]
            module_obj.uni_title = module["title"]
            module_obj.uni_competence = module["competence"]
            module_obj.uni_testUnits = module["testUnits"]
            module_obj.uni_priority = module["priority"]
            module_obj.uni_state = module["state"]
            module_obj.uni_approvedDate = module["approvedDate"]
            module_obj.uni_comment = module["comment"]
            module_obj.uni_file = module["file"]
            module_obj.uni_specialities = module["specialities"]
            module_obj.program = program
            module_obj.semester = semester
            module_obj.status = 'p'
            module_obj.save()
        else:
            print("Модуль не найден! Загрузите новую версию modules.json")

        program_module = ProgramModules.objects.filter(program=program, module=module_obj)
        if not program_module:
            program_module = ProgramModules(program=program, module=module_obj, semester=module_obj.semester,
                                            status="p")
            program_module.save()

        return module_obj, semester
