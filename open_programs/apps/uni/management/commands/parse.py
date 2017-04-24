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

            fulltime = False
            if 'зао' not in number:
                fulltime = True
            print("fulltime: ", fulltime)
            if fulltime:
                term = TrainingTerms.objects.filter(title="4 года").first()
                for module in [m for m in modules if m["disciplines"]]:
                    module_obj, semester = self.create_module(find_row_index_id, module, program)
                    semester = self.create_disciplines(find_row_index_id, module, module_obj, row, rows, semester, program, term)

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
                    self.create_disciplines_not_save(find_row_index_id, module, module_obj, row, rows, semester, program, term)


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
                ze = module["row"][find_row_index_id(f"EduVersionPlanTab.EduDisciplineList.__term{i}.__term{i}headerCell")]
                try:
                    if int(ze) > 0:
                        training_semester = i
                except:
                    pass
            except:
                pass

        try:
            semester_obj = Semester.filter(discipline=discipline, training_semester=training_semester).first()
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
                try:
                    discipline = Discipline.objects.get(title=d["title"])
                except:
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
        return semester

    def create_module(self, find_row_index_id, module, program):
        for i in range(10, 0, -1):
            try:
                ze = module["row"][find_row_index_id(f"EduVersionPlanTab.EduDisciplineList.__term{i}.__term{i}headerCell")]
                try:
                    if int(ze) > 0:
                        semester = i
                except:
                    pass
            except:
                pass
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
                                )
            module_obj.save()  # Создали модуль

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
                ze = module["row"][find_row_index_id(f"EduVersionPlanTab.EduDisciplineList.__term{i}.__term{i}headerCell")]
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

