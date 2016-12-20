from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.forms import ModelForm

from django.utils.translation import ugettext_lazy as _

from programs.models import Program
from courses.models import Course
from professions.models import Profession
from modules.models import Module
from disciplines.models import Discipline
from results.models import Result


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


def profession_detail(request, pk):
    context = {}
    context["title"] = _("Конструктор открытых образовательных программ")
    profession = Profession.objects.get(pk=pk)

    context["profession"] = profession
    return render(request, "constructor/profession.html", context)


def module_detail(request, pk):
    context = {}
    context["title"] = _("Конструктор открытых образовательных программ")
    module = Module.objects.get(pk=pk)
    disciplines = module.get_all_disciplines()

    disciplines_available = Discipline.objects.filter(module__isnull=True)


    context["module"] = module
    context["disciplines"] = disciplines
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
    discipline.module = module
    discipline.save()
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


def professions_edit(request, pk):
    profession = Profession.objects.get(pk=pk)

    #return redirect("discipline_detail", pk=disc_pk)


class ResultForm(ModelForm):
    class Meta:
        model = Result
        fields = ['title', ]


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ["title", "slug", "description", "about", "external_link", "type", "cover", "video", "video_cover", "workload", "points", "duration", "status"]


def course_detail(request, pk):
    context = {}
    context["title"] = _("Конструктор открытых образовательных программ")
    course = Course.objects.get(pk=pk)
    results_available = Result.objects.exclude(course__id=course.id)
    form = ResultForm

    context["course"] = course
    context["results_available"] = results_available
    context["form"] = form
    return render(request, "constructor/course.html", context)


def result_remove(request, course_pk, result_pk):
    course = Course.objects.get(pk=course_pk)
    result = Result.objects.get(pk=result_pk)
    course.results.remove(result)
    course.save()
    return redirect("course_detail", pk=course_pk)


def course_add_result(request, course_pk, result_pk):
    course = Course.objects.get(pk=course_pk)
    result = Result.objects.get(pk=result_pk)
    course.results.add(result)
    course.save()
    return redirect("course_detail", pk=course_pk)


def result_create(request, course_pk):
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.save()
            return redirect("course_add_result", course_pk=course_pk, result_pk=result.id)


# def course_create(request):
#     if request.method == 'POST':
#         form = CourseForm(request.POST)
#         if form.is_valid():
#             result = form.save(commit=False)
#             result.save()
#             return redirect("course_add_result", course_pk=course_pk, result_pk=result.id)
#
