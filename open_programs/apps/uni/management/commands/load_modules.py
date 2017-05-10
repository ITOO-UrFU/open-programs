from django.core.management.base import BaseCommand
import os
import json
from django.conf import settings
from modules.models import Module, Type
from disciplines.models import Discipline


class Command(BaseCommand):
    help = "Загрузка справочника модулей"

    def handle(self, *args, **options):
        def update_if_none(m, field, json_val=None):
            if json_val is None:
                return False
            if getattr(m, field) is None:
                m.__dict__[field] = json_val
                return True

        with open(os.path.join(settings.BASE_DIR, "uni_fixtures", "modules.json"), encoding='utf8') as basefile:
            fixtures = json.load(basefile)
            modules_len = len(fixtures)
            disc_generator = (len(d) for d in (mods for mods in fixtures))
            disciplines_len = sum(disc_generator)
            discipline_num = 1
            module_num = 1
            fieldset = (("description", "shortTitle"),
                      ("uni_uuid", "uuid"),
                      ("uni_number", "number"),
                      ("uni_coordinator", "coordinator"),
                      ("uni_type", "type"),
                      ("uni_title", "title"),
                      ("uni_competence", "competence"),
                      ("uni_testUnits", "testUnits"),
                      ("uni_priority", "priority"),
                      ("uni_state", "state"),
                      ("uni_approvedDate", "approvedDate"),
                      ("uni_comment", "comment"),
                      ("uni_specialities", "specialities"),
                      ("uni_file", "file"))

            for module in fixtures:
                print("Load modules: ", round(module_num / float(modules_len) * 100, 1), "%", sep='', end='\r', flush=True)
                m = Module.objects.filter(title=module["title"], uni_specialities=module["specialities"], uni_coordinator=module["coordinator"]).first()
                if m:
                    for field in fieldset:
                        update_if_none(m, field[0], module[field[1]])
                    if not m.type:
                        m.type = Type.objects.get(title="Модуль") if not "майнор" not in module["type"] else Type.objects.get(title="Майнор")
                    m.status = "p"
                    m.save()
                else:
                    m = Module(
                        title=module["title"],
                        type=Type.objects.get(title="Модуль") if not "майнор" not in module["type"] else Type.objects.get(title="Майнор"),
                        uni_number=module["number"],
                        uni_coordinator=module["coordinator"],
                        uni_competence=module["competence"],
                        uni_testUnits=module["testUnits"],
                        uni_priority=module["priority"],
                        uni_state=module["state"],
                        uni_approvedDate=module["approvedDate"],
                        uni_comment=module["comment"],
                        uni_file=module["file"],
                        uni_specialities=module["specialities"],
                        semester=99
                    )
                    m.save()
                module_num += 1

            for module in fixtures:
                print("Load disciplines: ", round(discipline_num / float(disciplines_len) * 100, 2), "%", sep='', end='\r',
                      flush=True)
                m = Module.objects.filter(title=module["title"], uni_specialities=module["specialities"],
                                          uni_coordinator=module["coordinator"]).first()
                disciplines = module["disciplines"]
                i = 1
                for discipline in disciplines:
                    d = Discipline.objects.filter(module=m, title=discipline["title"])
                    if not d and discipline["testUnits"] > 0:
                        d = Discipline(module=m,
                                       title=discipline["title"],
                                       labor=discipline["testUnits"],
                                       period=i,
                                       uni_uid=discipline["uid"],
                                       uni_discipline=discipline["discipline"],
                                       uni_number=discipline["number"],
                                       uni_section=discipline["section"],
                                       uni_file=discipline["file"])
                        d.save()
                    i += 1
                discipline_num += len(module["disciplines"])

