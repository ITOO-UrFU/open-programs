from django.http import Http404
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from programs.models import Program


@staff_member_required
def index(request):
    programs = Program.objects.all()
    return render(request, "stat/index.html", {"programs": programs})


@staff_member_required
def instance(request, id):
    program = Program.objects.get(pk=id)
    return render(request, "stats/program.html", {"program": program})
