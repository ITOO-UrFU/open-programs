from django.core.management.base import BaseCommand
import os
import json
from django.conf import settings
from modules.models import Module


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
            for module in fixtures:
                m = Module.objects.filter(title=module["title"]).first()
                if m:
                    for field in (("description", "shortTitle"),
                                  ("uni_uuid", "uid"),
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
                                  ("uni_file", "file")):
                        update_if_none(m, field[0], module[field[1]])
                m.save()