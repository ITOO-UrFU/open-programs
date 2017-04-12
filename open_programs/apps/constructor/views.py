from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.forms import ModelForm
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required

from django.utils.translation import ugettext_lazy as _

from programs.models import *
from courses.models import Course
from professions.models import Profession
from modules.models import Module
from disciplines.models import Discipline
from results.models import Result
from competences.models import Competence


@login_required
def index(request):
    context = {}
    context["title"] = _("Конструктор открытых образовательных программ")
    return render(request, "constructor/index.html", context)


@login_required
def programs(request):
    context = {}
    context["title"] = _("Конструктор открытых образовательных программ")
    programs = Program.objects.all()
    form = ProgramForm(request.POST)

    context["form"] = form
    context["programs"] = programs
    return render(request, "constructor/programs.html", context)


@login_required
def program_add(request, program_pk, module_pk):
    program = Program.objects.get(pk=program_pk)
    module = Module.objects.get(pk=module_pk)
    program.modules.add(module)
    program.save()
    return redirect("program_detail", pk=program_pk)


@login_required
def program_remove(request, program_pk, module_pk):
    program = Program.objects.get(pk=program_pk)
    module = Module.objects.get(pk=module_pk)
    program.modules.remove(module)
    program.save()
    return redirect("program_detail", pk=program_pk)


@login_required
def professions(request):
    context = {}
    context["title"] = _("Конструктор открытых образовательных программ")
    professions = Profession.objects.all()
    context["professions"] = professions
    return render(request, "constructor/professions.html", context)


@login_required
def courses(request):
    context = {}
    context["title"] = _("Конструктор открытых образовательных программ")
    courses = Course.objects.all()
    context["courses"] = courses
    return render(request, "constructor/courses.html", context)


@login_required
def program_detail(request, pk):
    context = {}
    context["title"] = _("Конструктор открытых образовательных программ")
    form = ModuleForm(request.POST)
    program = Program.objects.get(pk=pk)
    request.session['program'] = program.id.hex
    modules_available = Module.objects.exclude(program__id=program.id)

    context["form"] = form
    context["program"] = program
    context["modules_available"] = modules_available
    return render(request, "constructor/program.html", context)


@login_required
def module_detail(request, pk):
    context = {}
    form = DisciplineForm(request.POST)
    context["title"] = _("Конструктор открытых образовательных программ")
    module = Module.objects.get(pk=pk)
    disciplines = module.get_all_disciplines()
    if 'program' in request.session:
        context["program"] = Program.objects.get(id=request.session['program'])

    disciplines_available = Discipline.objects.filter(module__isnull=True)


    context["module"] = module
    context["form"] = form
    context["disciplines"] = disciplines
    context["disciplines_available"] = disciplines_available
    return render(request, "constructor/module.html", context)


@login_required
def discipline_remove(request, mod_pk, disc_pk):
    discipline = Discipline.objects.get(pk=disc_pk)
    discipline.delete()
    # discipline.module = None
    # discipline.save()
    return redirect("module_detail", pk=mod_pk)


@login_required
def discipline_add(request, mod_pk, disc_pk):
    module = Module.objects.get(pk=mod_pk)
    discipline = Discipline.objects.get(pk=disc_pk)
    discipline.module = module
    discipline.save()
    return redirect("module_detail", pk=mod_pk)


@login_required
def discipline_detail(request, pk):
    context = {}
    context["title"] = _("Конструктор открытых образовательных программ")
    discipline = Discipline.objects.get(pk=pk)
    courses_available = Course.objects.exclude(discipline__id=discipline.id)
    if 'program' in request.session:
        program = context["program"] = Program.objects.get(id=request.session['program'])

    context["program"] = program
    context["discipline"] = discipline
    context["courses_available"] = courses_available
    return render(request, "constructor/discipline.html", context)


@login_required
def course_remove(request, disc_pk, course_pk):
    discipline = Discipline.objects.get(pk=disc_pk)
    course = Course.objects.get(pk=course_pk)
    discipline.courses.remove(course)
    discipline.save()
    return redirect("discipline_detail", pk=disc_pk)


@login_required
def course_add(request, disc_pk, course_pk):
    discipline = Discipline.objects.get(pk=disc_pk)
    course = Course.objects.get(pk=course_pk)
    discipline.courses.add(course)
    discipline.save()
    return redirect("discipline_detail", pk=disc_pk)


class ResultForm(ModelForm):
    class Meta:
        model = Result
        fields = ['title', ]


class ProgramForm(ModelForm):
    class Meta:
        model = Program
        fields = ['title', ]


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ["title", "slug", "description", "about", "external_link", "type", "cover", "video", "video_cover", "workload", "points", "duration", "status"]


class CompetenceForm(ModelForm):
    class Meta:
        model = Competence
        fields = ['title', ]


class ProfessionForm(ModelForm):
    class Meta:
        model = Profession
        fields = ['title', 'description']


class DisciplineForm(ModelForm):
    class Meta:
        model = Discipline
        fields = ['title', "labor", "form"]


class ModuleForm(ModelForm):
    class Meta:
        model = Module
        fields = ["title"]


@login_required
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


@login_required
def result_remove(request, course_pk, result_pk):
    course = Course.objects.get(pk=course_pk)
    result = Result.objects.get(pk=result_pk)
    course.results.remove(result)
    course.save()
    return redirect("course_detail", pk=course_pk)


@login_required
def course_add_result(request, course_pk, result_pk):
    course = Course.objects.get(pk=course_pk)
    result = Result.objects.get(pk=result_pk)
    course.results.add(result)
    course.save()
    return redirect("course_detail", pk=course_pk)


@login_required
def result_create(request, course_pk):
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.save()
            return redirect("course_add_result", course_pk=course_pk, result_pk=result.id)


@login_required
def competence_result_create(request, comp_pk, prof_pk):
    if request.method == 'POST':
        competence = Competence.objects.get(pk=comp_pk)
        profession = Profession.objects.get(pk=prof_pk)
        form = ResultForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.save()
            competence.results.add(result)
            return redirect("profession_detail", pk=prof_pk)


@login_required
def competence_result_create_noprof(request, comp_pk):
    if request.method == 'POST':
        competence = Competence.objects.get(pk=comp_pk)
        form = ResultForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.save()
            competence.results.add(result)
            return redirect("competence_edit", pk=comp_pk)


@login_required
def competence_profession_remove(request, prof_pk, comp_pk):
    competence = Competence.objects.get(pk=comp_pk)
    competence.profession = None
    competence.save()
    return redirect("profession_detail", pk=prof_pk)


@login_required
def competence_profession_add(request, prof_pk, comp_pk):
    competence = Competence.objects.get(pk=comp_pk)
    competence.profession = Profession.objects.get(pk=prof_pk)
    competence.save()
    return redirect("profession_detail", pk=prof_pk)


@login_required
def competence_result_add(request, comp_pk, result_pk):
    competence = Competence.objects.get(pk=comp_pk)
    result = Result.objects.get(pk=result_pk)
    competence.results.add(result)
    competence.save()
    return redirect("competence_edit", pk=comp_pk)


@login_required
def competence_result_remove(request, comp_pk, result_pk):
    competence = Competence.objects.get(pk=comp_pk)
    result = Result.objects.get(pk=result_pk)
    competence.results.remove(result)
    competence.save()
    return redirect("profession_detail", pk=competence.profession.id)


@login_required
def competence_create(request, pk):
    profession = Profession.objects.get(pk=pk)
    if request.method == 'POST':
        form = CompetenceForm(request.POST)
        if form.is_valid():
            competence = form.save(commit=False)
            competence.profession = profession
            competence.save()
            return redirect("profession_detail", pk=pk)


@login_required
def course_create(request):
    context = {}
    context["title"] = _("Конструктор открытых образовательных программ")
    form = CourseForm(request.POST)
    context["form"] = form
    if request.method == 'POST':
        if form.is_valid():
            course = form.save(commit=False)
            course.save()
        return redirect("course_detail", pk=course.id)
    else:
        return render(request, "constructor/course_create.html", context)


@login_required
def profession_create(request):
    context = {}
    context["title"] = _("Конструктор открытых образовательных программ")
    form = ProfessionForm(request.POST)
    context["form"] = form
    if request.method == 'POST':
        if form.is_valid():
            profession = form.save(commit=False)
            profession.save()
        return redirect("profession_detail", pk=profession.id)
    else:
        return render(request, "constructor/profession_create.html", context)


@login_required
def competence_edit(request, pk):
    context = {}
    context["title"] = _("Конструктор открытых образовательных программ")
    competence = Competence.objects.get(pk=pk)
    if 'profession' in request.session:
        profession = context["profession"] = Profession.objects.get(id=request.session['profession'])
    results_available = Result.objects.exclude(competence__id=competence.id)
    form = ResultForm

    context["competence"] = competence
    context["profession"] = profession
    context["results_available"] = results_available
    context["form"] = form
    return render(request, "constructor/competence_edit.html", context)


@login_required
def profession_detail(request, pk):
    context = {}
    comp_form = CompetenceForm()
    result_form = ResultForm()
    context["comp_form"] = comp_form
    context["result_form"] = result_form
    context["title"] = _("Конструктор открытых образовательных программ")
    profession = Profession.objects.get(pk=pk)
    request.session['profession'] = profession.id
    competences_available = Competence.objects.filter(profession__isnull=True)

    context["profession"] = profession
    context["competences_available"] = competences_available
    return render(request, "constructor/profession.html", context)


@login_required
def discipline_create(request, module_pk):
    context = {}
    context["title"] = _("Конструктор открытых образовательных программ")
    form = DisciplineForm(request.POST)
    context["form"] = form
    if request.method == 'POST':
        if form.is_valid():
            discipline = form.save(commit=False)
            discipline.module = Module.objects.get(pk=module_pk)
            discipline.save()

    return redirect("module_detail", pk=module_pk)


@login_required
def module_create(request):
    context = {}
    context["title"] = _("Конструктор открытых образовательных программ")
    form = ModuleForm(request.POST)
    context["form"] = form
    if 'program' in request.session:
        program = context["program"] = Program.objects.get(id=request.session['program'])
    if request.method == 'POST':
        if form.is_valid():
            module = form.save(commit=False)
            module.save()
            program.modules.add(module)
            program.save()

    return redirect("program_detail", pk=program.id)


@login_required
def program_create(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            program = form.save(commit=False)
            program.save()
            return redirect("programs")


# @login_required def professions_edit(request, pk):
#     context = {}
#     profession = Profession.objects.get(pk=pk)
#     comp_form = CompetenceForm()
#     result_form = ResultForm()
#     context["comp_form"] = comp_form
#
#
#     #return redirect("discipline_detail", pk=disc_pk)