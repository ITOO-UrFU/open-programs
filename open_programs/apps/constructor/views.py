from django.shortcuts import render

from django.utils.translation import ugettext_lazy as _


def index(request):
    context = {}
    context["title"] = _("Конструктор открытых образовательных программ")
    return render(request, "constructor/index.html", context)
