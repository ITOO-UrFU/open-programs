import json

from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from programs.models import Program, ChoiceGroup


def index(request):
    context = dict()
    context["title"] = _("Конструктор")
    context["programs"] = Program.objects.filter(status="p", archived=False)

    return render(request, "constructor_v2/index.html", context)
