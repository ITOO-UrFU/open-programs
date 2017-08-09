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

        start_time = time.time()
        epp_json = options["epp_json"][0]
        program_title = options["program_title"][0]

        try:
            with open(epp_json, encoding='utf-8') as epp_json:
                epp = json.loads('\n'.join(epp_json.readlines()))
        except:
            raise FileNotFoundError

        try:
            program = Program.objects.filter(title=program_title).first()
            program.status = "p"
            program.save()
        except:
            raise NotImplementedError

            stage = epp["stage"]
            displayableTitle = epp["version"]
            number = epp["number"]
            active = epp["active"]
            title = epp["title"]

            term = epp["term"]

            lps = LearningPlan.objects.filter(uni_number=number, status="p")
            if len(lps) > 0:
                for lp in lps:
                    lp.uni_displayableTitle = displayableTitle
                    lp.uni_number = number
                    lp.uni_active = active
                    lp.uni_title = title
                    lp.uni_stage = stage
                    lp.uni_loadTimeType = loadTimeType
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
                                  uni_loadTimeType=loadTimeType,
                                  uni_html=json.dumps(epp),
                                  status="p"
                                  )
                lp.save()
                program.learning_plans.add(lp)
                program.save()

                #Добавили учебный план

            if term == 8:
                term = TrainingTerms.objects.filter(title="4 года").first()
                for epp_module in epp["modules"]:
                    module_obj, semester = self.create_module(epp_module, program)


                    semester = self.create_disciplines(find_row_index_id, module, module_obj, row, rows, semester,
                                                       program, term)

            else:
                years = 0
                for module in [m for m in modules]:
                    try:
                        for i in range(1, 10):
                            try:
                                ze = module["row"][
                                    find_row_index_id(
                                        f"EduVersionPlanTab.EduDisciplineList.__term{i}.__term{i}headerCell")]
                                try:
                                    if int(ze) > 0:
                                        latest_semester = i
                                except:
                                    latest_semester = i - 1
                            except:
                                pass
                        if latest_semester / float(2) > years:
                            years = latest_semester / float(2)
                    except:
                        pass

                if years == 5:
                    term = TrainingTerms.objects.filter(title="5 лет").first()
                else:
                    term = TrainingTerms.objects.filter(title="3,5 года").first()
                for module in [m for m in modules if m["disciplines"]]:
                    module_obj, semester = self.create_module_not_save(find_row_index_id, module, program)
                    self.create_disciplines_not_save(find_row_index_id, module, module_obj, row, rows, semester,
                                                     program, term)
        print(f"{self.bcolors.BOLD}--- {time.time() - start_time} секунд ---{self.bcolors.ENDC}")

    def create_semester(self, program, discipline, module, find_row_index_id, term):
        """
        1. ИД дисциплины
        2. Дисциплина.Программа
        3. Год текущий?
        4. Семестр: 0?
        5. Срок обучения (парсим)
        6. Семестр изучения (парсим как семестр модуля)
        :param program:
        :param discipline:
        :return:
        """
        for i in range(10, 0, -1):
            try:
                ze = module["row"][
                    find_row_index_id(f"EduVersionPlanTab.EduDisciplineList.__term{i}.__term{i}headerCell")]
                try:
                    if int(ze) > 0:
                        training_semester = i
                except:
                    pass
            except:
                training_semester = 99

        try:
            print(
                f"{self.bcolors.BOLD}Есть ли семестр дисциплины {discipline.title} / {training_semester} семестр ?{self.bcolors.ENDC}")
            semester_obj = Semester.filter(discipline=discipline, training_semester=training_semester).first()
            if semester_obj:
                print(f"{self.bcolors.OKGREEN}Ага.{self.bcolors.ENDC}")
        except:
            semester_obj = Semester(discipline=discipline,
                                    training_semester=training_semester,
                                    program=program,
                                    year='2017',
                                    admission_semester="0",
                                    term=term,
                                    )
            semester_obj.save()

    def create_disciplines(self, find_row_index_id, module, module_obj, row, rows, semester, program, term):
        for d in module["disciplines"]:
            if int(d["testUnits"]) > 0:
                for row in rows:
                    if d["title"] in row:
                        break

                print(
                    f"{self.bcolors.BOLD}Ищем дисциплину \"{d['title']}\" модуля \"{module_obj.title}\"!{self.bcolors.ENDC}")
                discipline = Discipline.objects.filter(title=d["title"],
                                                       module__in=Module.objects.filter(uni_uuid=module["uuid"]),
                                                       module__program=program).first()
                print(discipline)
                if discipline:
                    print(f"{self.bcolors.OKGREEN}Существует дисциплина {discipline.title}!{self.bcolors.ENDC}")
                else:
                    print(f"{self.bcolors.FAIL}Не существует дисциплины {d['title']}!!{self.bcolors.ENDC}")
                    discipline = Discipline(title=d["title"])

                for i in range(10, 0, -1):
                    try:
                        ze = row[
                            find_row_index_id(f"EduVersionPlanTab.EduDisciplineList.__term{i}.__term{i}headerCell")]
                        try:
                            if int(ze) > 0:
                                semester = i
                        except:
                            pass
                    except:
                        pass

                discipline.module = module_obj
                discipline.labor = d["testUnits"]
                discipline.uni_uid = d["uid"]
                discipline.uni_discipline = d["discipline"]
                discipline.uni_number = d["number"]
                discipline.uni_section = d["section"]
                discipline.uni_file = d["file"]
                discipline.period = semester - module_obj.semester + 1
                try:
                    try:
                        if int(max(row[5].split("-"))):
                            discipline.form = "z"
                    except:
                        pass
                    try:
                        if int(max(row[4].split("-"))):
                            discipline.form = "e"
                    except:
                        pass
                except:
                    pass

                discipline.status = "p"
                discipline.save()
                self.create_semester(program, discipline, module, find_row_index_id, term)
                print(f"{self.bcolors.OKBLUE}{discipline.title}{self.bcolors.ENDC}")
        return semester

    def create_module(self, module, program):
        for i in range(10, 0, -1):
            try:
                ze = module["row"][
                    find_row_index_id(f"EduVersionPlanTab.EduDisciplineList.__term{i}.__term{i}headerCell")]
                try:
                    if int(ze) > 0:
                        semester = i
                except:
                    pass
            except:
                semester = 99
        try:
            module_obj = Module.objects.filter(title=module["title"]).first()
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
        except:
            module_obj = Module(title=module["title"],
                                uni_uuid=module["uuid"],
                                uni_number=module["number"],
                                uni_coordinator=module["coordinator"],
                                uni_type=module["type"],
                                uni_title=module["title"],
                                uni_competence=module["competence"],
                                uni_testUnits=module["testUnits"],
                                uni_priority=module["priority"],
                                uni_state=module["state"],
                                uni_approvedDate=module["approvedDate"],
                                uni_comment=module["comment"],
                                uni_file=module["file"],
                                uni_specialities=module["specialities"],
                                program=program,
                                semester=semester,
                                status='p',
                                )
            module_obj.save()  # Создали модуль

        program_module = ProgramModules.objects.filter(program=program, module=module_obj)
        if not program_module:
            program_module = ProgramModules(program=program, module=module_obj, semester=module_obj.semester,
                                            status="p")
            program_module.save()

        return module_obj, semester

    def create_disciplines_not_save(self, find_row_index_id, module, module_obj, row, rows, semester, program, term):
        if module_obj is not None:
            for d in module["disciplines"]:
                discipline = None
                if int(d["testUnits"]) > 0:
                    for row in rows:
                        if d["title"] in row:
                            break
                    try:
                        discipline = Discipline.objects.get(title=d["title"])
                    except:
                        print("Unknown discipline: ", d["title"])

                    for i in range(10, 0, -1):
                        try:
                            ze = row[
                                find_row_index_id(f"EduVersionPlanTab.EduDisciplineList.__term{i}.__term{i}headerCell")]
                            try:
                                if int(ze) > 0:
                                    semester = i
                            except:
                                pass
                        except:
                            pass

                    if discipline:
                        self.create_semester(program, discipline, module, find_row_index_id, term)
            return semester

    def create_module_not_save(self, find_row_index_id, module, program):
        for i in range(10, 0, -1):
            try:
                ze = module["row"][
                    find_row_index_id(f"EduVersionPlanTab.EduDisciplineList.__term{i}.__term{i}headerCell")]
                try:
                    if int(ze) > 0:
                        semester = i
                except:
                    pass
            except:
                pass
        try:
            module_obj = Module.objects.filter(title=module["title"]).first()

        except:
            print("Unknown module: ", module["title"])

        return module_obj, semester

    def decompose(self, soup, tag, classname):
        [el.decompose() for el in soup.find_all(tag, {'class': classname})]
