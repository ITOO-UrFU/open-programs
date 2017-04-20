from bs4 import BeautifulSoup
import csv
import os
import re
import json
import pprint

from django.core.management.base import BaseCommand

from programs.models import Program, ProgramModules, LearningPlan
from disciplines.models import Discipline
from modules.models import Module

pp = pprint.PrettyPrinter(indent=4)


class Command(BaseCommand):
    help = "Create Django objects from raw&ugly UrFU data."
    requires_system_checks = True
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('html_path', nargs=1)
        parser.add_argument('uni_modules_path', nargs=1)
        parser.add_argument('programs_path', nargs=1)
        parser.add_argument('program_title', nargs=1)

    def handle(self, *args, **options):
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
            programs_soup = BeautifulSoup(raw_programs, 'html.parser')
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

        try:
            program = Program.objects.filter(title=program_title).first()
            program.status = "p"
            program.save()
        except:
            raise NotImplementedError

        if raw_html:
            soup = BeautifulSoup(raw_html, 'html.parser')
            [s.extract() for s in soup('script')]
            [s.extract() for s in soup('style')]
            self.decompose(soup, "table", "menu_table")
            self.decompose(soup, "td", "navpath")
            self.decompose(soup, "div", "buttons")
            soup.find('td', id="nav_td").decompose()

            stage = soup.find('td', id="EduVersionPlanTab.EduVersionPlan.stage").text.strip().lower() == "утверждено"
            displayableTitle = soup.find('td', id="EduVersionPlanTab.EduVersionPlan.displayableTitle").text.strip()
            number = soup.find('td', id="EduVersionPlanTab.EduVersionPlan.number").text.strip()
            active = soup.find('td', id="EduVersionPlanTab.EduVersionPlan.active").text.strip()
            title = soup.find('td', id="EduVersionPlanTab.EduVersionPlan.title").text.strip()
            loadTimeType = soup.find("td", id="EduVersionPlanTab.EduVersionPlan.loadTimeType").text.strip()
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

            if 'зао' not in number:
                fulltime = True

            table = soup.find('table', id="EduVersionPlanTab.EduDisciplineList")
            headers = [header.text.strip() for header in table.find_all('th')]
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

            for module in [m for m in modules if m["disciplines"]]:
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
                                        uni_specialities=module["specialities"]
                                        )
                    module_obj.save()  # Создали модуль





                # Ищем дисциплины
                for d in module["disciplines"]:
                    if int(d["testUnits"]) > 0:
                        try:
                            discipline = Discipline.objects.get(title=d["title"])
                        except:
                            discipline = Discipline(title=d["title"])
                            discipline.module = module_obj
                            discipline.labor = d["testUnits"]

                            discipline.uni_uid = d["uid"]
                            discipline.uni_discipline = d["discipline"]
                            discipline.uni_number = d["number"]
                            discipline.uni_section = d["section"]
                            discipline.uni_file = d["file"]

                            discipline.status = "p"
                            discipline.save()

            # Собираем группу выбора

            # pm = ProgramModules(program=program,
            #                     module=module_obj)  # TODO: ChoiceGroup
            # pm.save()

    def decompose(self, soup, tag, classname):
        [el.decompose() for el in soup.find_all(tag, {'class': classname})]

