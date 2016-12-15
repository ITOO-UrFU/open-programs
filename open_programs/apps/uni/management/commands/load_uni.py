from django.core.management.base import BaseCommand
import os
import json
from django.conf import settings
from uni.models import *


class Command(BaseCommand):
    help = "Загрузка справочника направлений"

    def handle(self, *args, **options):
        with open(os.path.join(settings.BASE_DIR, "uni_fixtures", "specialities.json"), encoding='utf8') as basefile:
            fixtures = json.load(basefile)
            for speciality in fixtures:
                spec = Speciality(uid=speciality["uid"],
                                  okso=speciality["okso"],
                                  title=speciality["title"],
                                  ministerialCode=speciality["ministerialCode"],
                                  ugnTitle=speciality["ugnTitle"],
                                  standard=speciality["standard"])
                spec.save()






