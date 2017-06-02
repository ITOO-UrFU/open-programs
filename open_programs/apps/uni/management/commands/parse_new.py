from bs4 import BeautifulSoup
import re
import json
import time

from django.core.management.base import BaseCommand

from programs.models import Program, ProgramModules, LearningPlan
from disciplines.models import Discipline, Semester, TrainingTerms
from modules.models import Module


class Command(BaseCommand):
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
                    print(f"{self.bcolors.BOLD}Есть ли программа \"{row[1]}\"?{self.bcolors.ENDC}")
                    program = Program.objects.get(title=row[1])
                    if program:
                        print(f"{self.bcolors.OKGREEN}Ага.{self.bcolors.ENDC}")
                except:
                    print(f"{self.bcolors.WARNING}Нет, создаём.{self.bcolors.ENDC}")

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
                    if m:
                        for module in modules_json:
                            if str(module["number"]) == str(m.group(0)):
                                module["row"] = row
                                modules.append(module)

            print(json.dumps(modules))