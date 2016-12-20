from django.shortcuts import render, redirect

from django.utils.translation import ugettext_lazy as _

from programs.models import Program
from courses.models import Course
from professions.models import Profession
from modules.models import Module
from disciplines.models import Discipline


def index(request):
    context = {}
    context["title"] = _("Конструктор открытых образовательных программ")
    return render(request, "constructor/index.html", context)


def programs(request):
    context = {}
    context["title"] = _("Конструктор открытых образовательных программ")
    programs = Program.objects.filter(status="p", archived=False)

    context["programs"] = programs
    return render(request, "constructor/programs.html", context)


def program_add(request, program_pk, module_pk):
    program = Program.objects.get(pk=program_pk)
    module = Module.objects.get(pk=module_pk)
    program.modules.add(module)
    program.save()
    return redirect("program_detail", pk=program_pk)


def program_remove(request, program_pk, module_pk):
    program = Program.objects.get(pk=program_pk)
    module = Module.objects.get(pk=module_pk)
    program.modules.remove(module)
    program.save()
    return redirect("program_detail", pk=program_pk)


def professions(request):
    context = {}
    context["title"] = _("Конструктор открытых образовательных программ")
    professions = Profession.objects.filter(status="p", archived=False)
    context["professions"] = professions
    return render(request, "constructor/professions.html", context)


def courses(request):
    context = {}
    context["title"] = _("Конструктор открытых образовательных программ")
    courses = Course.objects.filter(status="p", archived=False)
    context["courses"] = courses
    return render(request, "constructor/courses.html", context)


def program_detail(request, pk):
    context = {}
    context["title"] = _("Конструктор открытых образовательных программ")
    program = Program.objects.get(pk=pk)
    modules_available = Module.objects.exclude(program__id=program.id)

    context["program"] = program
    context["modules_available"] = modules_available
    return render(request, "constructor/program.html", context)


def module_detail(request, pk):
    context = {}
    context["title"] = _("Конструктор открытых образовательных программ")
    module = Module.objects.get(pk=pk)

    disciplines_available = Discipline.objects.exclude(module__id=module.id)


    context["module"] = module
    context["disciplines_available"] = disciplines_available
    return render(request, "constructor/module.html", context)


def discipline_remove(request, mod_pk, disc_pk):
    module = Module.objects.get(pk=mod_pk)
    discipline = Discipline.objects.get(pk=disc_pk)
    module.disciplines.remove(discipline)
    module.save()
    return redirect("module_detail", pk=mod_pk)


def discipline_add(request, mod_pk, disc_pk):
    module = Module.objects.get(pk=mod_pk)
    discipline = Discipline.objects.get(pk=disc_pk)
    module.disciplines.add(discipline)
    module.save()
    return redirect("module_detail", pk=mod_pk)


def discipline_detail(request, pk):
    context = {}
    context["title"] = _("Конструктор открытых образовательных программ")
    discipline = Discipline.objects.get(pk=pk)
    courses_available = Course.objects.exclude(discipline__id=discipline.id)

    context["discipline"] = discipline
    context["courses_available"] = courses_available
    return render(request, "constructor/discipline.html", context)


def course_remove(request, disc_pk, course_pk):
    discipline = Discipline.objects.get(pk=disc_pk)
    course = Course.objects.get(pk=course_pk)
    discipline.courses.remove(course)
    discipline.save()
    return redirect("discipline_detail", pk=disc_pk)


def course_add(request, disc_pk, course_pk):
    discipline = Discipline.objects.get(pk=disc_pk)
    course = Course.objects.get(pk=course_pk)
    discipline.courses.add(course)
    discipline.save()
    return redirect("discipline_detail", pk=disc_pk)
