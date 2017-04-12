import os
import json
import os
import pyodbc


DUMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dump")

if 'accdb' in pyodbc.dataSources():
    if not os.path.isfile('C:\\Projects\\OOP_feb\\open-programs\\utils\\3.accdb'):
        print('Файл базы данных не найден')
    else:
        connection = pyodbc.connect("DSN=accdb")
        print('Connection: ok')

cur = connection.cursor()

tables = [t.table_name for t in cur.tables(tableType='TABLE')]
print(tables)


cur.execute("SELECT * FROM [Образовательные программы]")
print()

while True:
    row = cur.fetchone()
    if row is None:
        break
    Program = {}
    Program["model"] = "programs.program"
    Program["pk"] = row.get("Код ОП")
    Program["fields"] = {}
    Program["fields"]["title"] = row.get("Наименование программы")
    Program["fields"]["training_direction"] = row.get("Направление подготовки")
    Program["fields"]["archived"] = False
    Program["fields"]["created"] = "2017-02-21T12:25:49.862Z"
    Program["fields"]["updated"] = "2017-02-21T12:25:49.862Z"
    Program["fields"]["status"] = "p"
    Program["fields"]["level"] = "b"
    Program["fields"]["chief"] = 1
    Program["fields"]["competences"] = []

    PROGRAMS.append(Program)

cur.close()
print(PROGRAMS)

#
# #### Образовательные цели
# cur = conn.cursor()
# cur.execute("SELECT * FROM [Образовательные цели]")
#
# while True:
#     row = cur.fetchone()
#     if row is None:
#         break
#     TrainingTarget = {}
#     print(row)
# cur.close()
#
#
#
#
# #### Группы выбора
# cur = conn.cursor()
# cur.execute("SELECT * FROM [Группы выбора]")
# while True:
#     row = cur.fetchone()
#     if row is None:
#         break
#     TrainingTarget = {}
#     print(row)
# cur.close()
#
#
#
# #### Модули программы
# cur = conn.cursor()
# cur.execute("SELECT * FROM [Модули программы]")
#
# while True:
#     row = cur.fetchone()
#     if row is None:
#         break
#     ProgramModules = {}
#     ProgramModules["model"] = ["programs.programmodules"]
#     ProgramModules["pk"] = row.get("Код модуля")
#     ProgramModules["fields"][""] =
# cur.close()
#
#
# #### Модули цели
# cur = conn.cursor()
# cur.execute("SELECT * FROM [Модули цели]")
#
# while True:
#     row = cur.fetchone()
#     if row is None:
#         break
#     TrainingTarget = {}
#     print(row)
# cur.close()
#
#

#### Модули
# MODULES = []
#
# cur = conn.cursor()
# cur.execute("SELECT * FROM [Модули]")
#
# while True:
#     row = cur.fetchone()
#     if row is None:
#         break
#     Module = {}
#     Module["model"] = "modules.module"
#     Module["pk"] = row.get("Код модуля")
#     Module["fields"] = {}
#     Module["fields"]["archived"] = False
#     Module["fields"]["created"] = "2017-02-20T07:01:43.361Z"
#     Module["fields"]["updated"] = "2017-02-20T07:01:43.361Z"
#     Module["fields"]["status"] = "p"
#     Module["fields"]["title"] = row.get("Наименование модуля")
#     Module["fields"]["description"] = ""
#     Module["fields"]["type"] = 1
#     Module["fields"]["results_text"] = ""
#     Module["fields"]["semester"] = 1
#     Module["fields"]["results"] = []
#     Module["fields"]["competences"] = []
#
#     MODULES.append(Module)
#
# cur.close()

# #### Дисциплины
# import uuid
# Disciplines = []
#
# cur = conn.cursor()
# cur.execute("SELECT * FROM [Дисциплины]")
#
# while True:
#     row = cur.fetchone()
#     if row is None:
#         break
#     Discipline = {}
#     Discipline["model"] = "disciplines.discipline"
#     # Discipline["pk"] = str(uuid.uuid4())
#     Discipline["fields"] = {}
#     Discipline["fields"]["archived"] = False
#     Discipline["fields"]["created"] = "2017-02-20T07:01:43.361Z"
#     Discipline["fields"]["updated"] = "2017-02-20T07:01:43.361Z"
#     Discipline["fields"]["status"] = "p"
#     Discipline["fields"]["name"] = row.get("Наименование дисциплины")
#     Discipline["fields"]["description"] = ""
#     Discipline["fields"]["module"] = row.get("Код модуля")
#     Discipline["fields"]["labor"] = row.get("Трудоемкость дисциплины")
#
#     Discipline["fields"]["period"] = row.get("Период освоения в модуле")
#     Discipline["fields"]["form"] = row.get("Форма контроля")
#     Discipline["fields"]["results_text"] = ""
#     Discipline["fields"]["courses"] = []
#     Discipline["fields"]["results"] = []
#
#     Disciplines.append(Discipline)
#
# cur.close()
#
# conn.close()

# print(json.dumps(Disciplines))

