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
                    m.uni_uuid = module["uuid"]
                m = Module()
                m.save()