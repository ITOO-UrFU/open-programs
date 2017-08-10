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

        print("Semesters count: ", term)

        for epp_module in epp["modules"]:
            module_obj, semester = self.create_module(epp_module, program, term)

    def create_module(self, epp_module, program, term):
        semester = min([int(d["firstSemester"]) for d in epp_module["disciplines"]])
        module_obj = Module.objects.filter(uni_number=epp_module["disciplineNumberheaderCell"]).first()

        if module_obj and term == 8:
            module_obj.uni_uuid = epp_module["uuid"]
            module_obj.uni_number = epp_module["disciplineNumberheaderCell"]
            module_obj.uni_coordinator = epp_module["coordinator"]
            module_obj.uni_type = epp_module["type"]
            module_obj.uni_title = epp_module["title"]
            module_obj.uni_testUnits = epp_module["testUnits"]
            module_obj.uni_priority = epp_module["priority"]
            module_obj.uni_state = epp_module["state"]
            module_obj.uni_comment = epp_module["comment"]
            module_obj.uni_file = epp_module["file"]
            module_obj.uni_specialities = epp_module["specialities"]
            module_obj.program = program
            module_obj.semester = semester
            module_obj.status = 'p'
            module_obj.save()

            program_module = ProgramModules.objects.filter(program=program, module=module_obj)
            if not program_module:
                program_module = ProgramModules(program=program, module=module_obj, semester=module_obj.semester,
                                                status="p", index=epp_module["indexheaderCell"])
                program_module.save()

            for_delete = []

            for epp_discipline in epp_module["disciplines"]:
                discipline = Discipline.objects.filter(module=module_obj,
                                                       title=epp_discipline['titleheaderCell']).first()
                if not discipline:
                    discipline = Discipline.objects.filter(module=module_obj,
                                                           title__contains=epp_discipline['titleheaderCell']).first()

                training_semester = int(epp_discipline["firstSemester"])
                if Discipline.objects.filter(module=module_obj, title=epp_discipline['titleheaderCell']).count() == 0:
                    for_delete.append(discipline.id)

                try:
                    if epp_discipline["exam"] > epp_discipline["credit"]:
                        form = "e"
                    else:
                        form = "z"
                except:
                    print(epp_discipline)

                print(epp_discipline['titleheaderCell'])
                parted_discipline = Discipline.objects.filter(title=epp_discipline['titleheaderCell'],
                                                              module=module_obj, status="p",
                                                              archived=False).first()

                if not parted_discipline:
                    parted_discipline = Discipline.objects.create(
                        title=epp_discipline['titleheaderCell'],
                        description=discipline.description,
                        module=module_obj,
                        labor=epp_discipline["gosLoadInTestUnitsheaderCell"],
                        period=training_semester - semester + 1,
                        form=form,
                        uni_uid=discipline.uni_uid,
                        uni_discipline=discipline.uni_discipline,
                        uni_number=discipline.uni_number,
                        uni_section=discipline.uni_section,
                        uni_file=discipline.uni_file,
                        status="p"
                    )

                if term == 8:
                    cur_term = TrainingTerms.objects.filter(title="4 года").first()
                elif term == 10:
                    cur_term = TrainingTerms.objects.filter(title="5 лет").first()
                elif term == 7:
                    cur_term = TrainingTerms.objects.filter(title="3,5 года").first()

                semester_obj = Semester.objects.filter(discipline=discipline, training_semester=training_semester,
                                                       program=program, term=cur_term).first()
                if not semester_obj:
                    semester_obj = Semester.objects.create(discipline=discipline,
                                                           training_semester=training_semester,
                                                           program=program,
                                                           year='2017',
                                                           admission_semester="0",
                                                           term=cur_term,
                                                           )

            Discipline.objects.filter(id__in=for_delete).delete()
        else:
            print("Модуль не найден! Загрузите новую версию modules.json")

        return module_obj, semester
