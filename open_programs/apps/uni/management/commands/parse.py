from bs4 import BeautifulSoup
import csv
import os
import re
import json

from django.core.management.base import BaseCommand

from programs.models import Program


class Command(BaseCommand):
    help = "Create Django objects from raw&ugly UrFU data."
    requires_system_checks = True
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('html_path', nargs=1)
        parser.add_argument('uni_modules_path', nargs=1)
        parser.add_argument('program_title', nargs=1)

    def handle(self, *args, **options):
        html_path = options["html_path"][0]
        uni_modules_path = options["uni_modules_path"][0]
        program_title = options["program_title"][0]

        try:
            program = Program.objects.get(title=program_title)
        except:
            program = Program(title=program_title,
                              training_direction='Направление подготовки',  # TODO: find this
                              level='b',  # TODO: find this
                              )
            program.save()

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

        if raw_html:
            soup = BeautifulSoup(raw_html, 'html.parser')
            [s.extract() for s in soup('script')]
            [s.extract() for s in soup('style')]
            self.decompose(soup, "table", "menu_table")
            self.decompose(soup, "td", "navpath")
            self.decompose(soup, "div", "buttons")
            soup.find('td', id="nav_td").decompose()

            if soup.find('td', id="EduVersionPlanTab.EduVersionPlan.stage").text.strip().lower() == "утверждено":
                print("План утверждён")
                stage = True

            displayableTitle = soup.find('td', id="EduVersionPlanTab.EduVersionPlan.displayableTitle").text.strip()
            number = soup.find('td', id="EduVersionPlanTab.EduVersionPlan.number").text.strip()
            active = soup.find('td', id="EduVersionPlanTab.EduVersionPlan.active").text.strip()
            title = soup.find('td', id="EduVersionPlanTab.EduVersionPlan.title").text.strip()

            print("Версия:", displayableTitle, sep=" ")
            print("Номер УП:", number, sep=" ")
            print("Текущая версия:", active, sep=" ")
            print("Название:", title, sep=" ")

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
                        [modules.append(module) for module in modules_json if str(module["number"]) == str(m.group(0))]

            print(len(modules))

    def decompose(self, soup, tag, classname):
        [el.decompose() for el in soup.find_all(tag, {'class': classname})]

