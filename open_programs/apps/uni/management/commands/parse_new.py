from bs4 import BeautifulSoup
import re
import json
import time

from django.core.management.base import BaseCommand

from programs.models import Program, ProgramModules, LearningPlan
from disciplines.models import Discipline, Semester, TrainingTerms
from modules.models import Module


class Command(BaseCommand):
    """
    Example: ./manage.py parse_new "/home/developer/КТОМ 4.html" uni_fixtures/modules.json ./get_programs.html "Конструкторско-технологическое обеспечение машиностроительных производств"
    """
    help = "Create Django objects from raw&ugly UrFU data."
    requires_system_checks = True
    requires_migrations_checks = True

    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    def decompose(self, soup, tag, classname):
        [el.decompose() for el in soup.find_all(tag, {'class': classname})]

    def add_arguments(self, parser):
        parser.add_argument('html_path', nargs=1)
        parser.add_argument('uni_modules_path', nargs=1)
        parser.add_argument('programs_path', nargs=1)
        parser.add_argument('program_title', nargs=1)

    def handle(self, *args, **options):

        start_time = time.time()
        html_path = options["html_path"][0]
        uni_modules_path = options["uni_modules_path"][0]
        program_title = options["program_title"][0]
        programs_path = options["programs_path"][0]

        try:
            with open(html_path, encoding='utf-8') as html_file:
                raw_html = '\n'.join(html_file.readlines())
        except:
            raise FileNotFoundError

        try:
            with open(uni_modules_path, encoding='utf-8') as modules_file:
                modules_json = json.load(modules_file)
        except:
            raise FileNotFoundError

        try:
            with open(programs_path, encoding='utf-8') as programs_file:
                raw_programs = '\n'.join(programs_file.readlines())
        except:
            raise FileNotFoundError

        if raw_programs:
            programs_soup = BeautifulSoup(raw_programs, 'lxml')
            rows = []
            for row in programs_soup.find_all('tr', {"class": "main-info"}):
                rows.append([val.text.strip() for val in row.find_all('td')])

            for row in rows:
                try:
                    program = Program.objects.get(title=row[1])
                except:
                    def level(x):
                        return {
                            'Магистр'.lower() in str(x).lower(): "m",
                            'Специалист'.lower() in str(x).lower(): "s",
                            'Бакалавр'.lower() in str(x).lower(): "b",
                        }[True]
                    program = Program(title=row[1],
                                      training_direction=row[2],
                                      level=level(row[4]),
                                      )
                    program.save()
                    print(f"{self.bcolors.BOLD}Создана программа программа \"{row[1]}\"?{self.bcolors.ENDC}")

        try:
            program = Program.objects.filter(title=program_title).first()
            program.status = "p"
            program.save()
        except:
            raise NotImplementedError

        if raw_html:
            soup = BeautifulSoup(raw_html, 'lxml')
            [s.extract() for s in soup('script')]
            [s.extract() for s in soup('style')]
            self.decompose(soup, "table", "menu_table")
            self.decompose(soup, "td", "navpath")
            self.decompose(soup, "div", "buttons")
            soup.find('td', id="nav_td").decompose()

            try:
                stage = soup.find('td', id="EduVersionPlanTab.EduVersionPlan.stage").text.strip().lower() == "утверждено"
            except:
                stage = False
            try:
                displayableTitle = soup.find('td', id="EduVersionPlanTab.EduVersionPlan.displayableTitle").text.strip()
            except:
                displayableTitle = ""
            try:
                number = soup.find('td', id="EduVersionPlanTab.EduVersionPlan.number").text.strip()
            except:
                number = ""
            try:
                active = soup.find('td', id="EduVersionPlanTab.EduVersionPlan.active").text.strip()
            except:
                active = "нет"
            try:
                title = soup.find('td', id="EduVersionPlanTab.EduVersionPlan.title").text.strip()
            except:
                title = ""
            try:
                loadTimeType = soup.find("td", id="EduVersionPlanTab.EduVersionPlan.loadTimeType").text.strip()
            except:
                loadTimeType = "часов в неделю"

            html = soup.find("table", {"class": "basic"}).prettify()

            lps = LearningPlan.objects.filter(uni_number=number, status="p")
            if len(lps) > 0:
                for lp in lps:
                    lp.uni_displayableTitle = displayableTitle
                    lp.uni_number = number
                    lp.uni_active = active
                    lp.uni_title = title
                    lp.uni_stage = stage
                    lp.uni_loadTimeType = loadTimeType
                    lp.uni_html = html
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
                                  uni_html=html,
                                  status="p"
                                  )
                lp.save()
                program.learning_plans.add(lp)
                program.save()

            table = soup.find('table', id="EduVersionPlanTab.EduDisciplineList")
            headers = [header.text.strip() for header in table.find_all('th')]

            def find_row_index(row_text):
                headers = table.find_all('th')
                return headers.index(table.find('th', text=row_text))

            def find_row_index_id(id):
                headers = table.find_all('th')
                return headers.index(table.find('th', id=id))


            rows = []
            for row in table.find_all('tr'):
                rows.append([val.text.strip() for val in row.find_all('td')])

            # Ищем модули
            modules = []
            for header in headers:
                if "Номер модуля, дисциплины".lower() == header.lower():
                    module_numbers_col = headers.index(header)

            for row in rows:
                if row:
                    m = re.search('\d\d+', row[module_numbers_col])
                    if m and "М" in row[1]:
                        for module in modules_json:
                            if str(module["number"]) == str(m.group(0)):
                                print(str(module["number"]), str(m.group(0)), str(module["number"]) == str(m.group(0)))
                                module["row"] = row
                                modules.append(module)

            program_modules = ProgramModules.objects.filter(program=program)

            for module in modules:
                print("            ", module['title'])
                if program_modules.filter(module__uni_uuid=module["uuid"]):
                    print(f"Модуль есть: {module['title']}")

            fulltime = False
            if 'зао' not in number:
                fulltime = True
            print("fulltime: ", fulltime)
            if fulltime:
                term = TrainingTerms.objects.filter(title="4 года").first()
                for module in [m for m in modules if m["disciplines"]]:
                    module_obj, semester = self.create_module(find_row_index_id, module, program)



    def create_module(self, find_row_index_id, module, program):
        print(f"Ищем или создаём модуль: {module['title']}")
        for i in range(10, 0, -1):
            try:
                ze = module["row"][find_row_index_id(f"EduVersionPlanTab.EduDisciplineList.__term{i}.__term{i}headerCell")]
                try:
                    if int(ze) > 0:
                        semester = i
                except:
                    pass
            except:
                semester = 99
        print(f"Семестр: {semester}")
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
            print(f"{self.bcolors.OKBLUE}Модуль найден: {module['title']}{self.bcolors.ENDC}")
        except:
            print(f"{self.bcolors.BOLD}Модуль создан: {module['title']}{self.bcolors.ENDC}")
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
            module_obj.save()

        program_module = ProgramModules.objects.filter(program=program, module=module_obj)
        if not program_module:
            program_module = ProgramModules(program=program, module=module_obj, semester=module_obj.semester, status="p")
            program_module.save()

        return module_obj, semester