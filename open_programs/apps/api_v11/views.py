from datetime import date
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, CreateAPIView

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from courses.models import Course, Session
from persons.models import Person
from competences.models import Competence
from results.models import Result
from disciplines.models import Discipline, Semester, TrainingTerms, Diagram, Technology, Variant
from modules.models import Module, Type
from programs.models import Program, TrainingTarget, ProgramCompetence, ProgramModules, \
                            TargetModules, ChoiceGroup, ChoiceGroupType, Changed

from courses.serializers import CourseSerializer, SessionSerializer, CourseIdSerializer
from persons.serializers import UserSerializer, PersonSerializer
from competences.serializers import CompetenceSerializer
from results.serializers import ResultSerializer
from modules.serializers import ModuleSerializer, TypeSerializer
from programs.serializers import ProgramSerializer, TrainingTargetSerializer, \
                                 ProgramCompetenceSerializer, ChoiceGroupTypeSerializer, \
                                 ChoiceGroupSerializer, ProgramModulesSerializer, TargetModulesSerializer
from disciplines.serializers import *

from cms.api_views import *

from django.core.cache import cache


class ProgramList(viewsets.ModelViewSet):
    queryset = Program.objects.filter(status="p", archived=False)
    serializer_class = ProgramSerializer


class ModuleList(viewsets.ModelViewSet):
    queryset = Module.objects.filter(status="p", archived=False)
    serializer_class = ModuleSerializer


class TypeList(viewsets.ModelViewSet):
    queryset = Type.objects.filter(status="p", archived=False)
    serializer_class = TypeSerializer


class DisciplineList(viewsets.ModelViewSet):
    queryset = Discipline.objects.filter(status="p", archived=False)
    serializer_class = DisciplineSerializer


class ResultList(viewsets.ModelViewSet):
    queryset = Result.objects.filter(status="p", archived=False)
    serializer_class = ResultSerializer


class CompetenceList(viewsets.ModelViewSet):
    queryset = Competence.objects.filter(status="p", archived=False)
    serializer_class = CompetenceSerializer


class CompetenceListCreateView(ListCreateAPIView):
    model = Competence
    serializer_class = CompetenceSerializer

    def create(self, request, *args, **kwargs):
        data = request.DATA

        c = Competence.objects.create(title=data["title"], status="p",results=Result.objects.get)

        # ... create nested objects from request data ...

        # ...
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class PersonList(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class CourseList(viewsets.ModelViewSet):
    queryset = Course.objects.filter(status="p", archived=False)
    serializer_class = CourseSerializer


class UserList(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TrainingTargetList(viewsets.ModelViewSet):
    queryset = TrainingTarget.objects.filter(status="p", archived=False)
    serializer_class = TrainingTargetSerializer


class ProgramCompetenceList(viewsets.ModelViewSet):
    queryset = ProgramCompetence.objects.filter(status="p", archived=False)
    serializer_class = ProgramCompetenceSerializer


class ProgramModulesList(viewsets.ModelViewSet):
    queryset = ProgramModules.objects.filter(status="p", archived=False)
    serializer_class = ProgramModulesSerializer


class TargetModulesList(viewsets.ModelViewSet):
    queryset = TargetModules.objects.filter(status="p", archived=False)
    serializer_class = TargetModulesSerializer


class ChoiceGroupList(viewsets.ModelViewSet):
    queryset = ChoiceGroup.objects.filter(status="p", archived=False)
    serializer_class = ChoiceGroupSerializer


class ChoiceGroupTypeList(viewsets.ModelViewSet):
    queryset = ChoiceGroupType.objects.filter(status="p", archived=False)
    serializer_class = ChoiceGroupTypeSerializer


class DiagramList(viewsets.ModelViewSet):
    queryset = Diagram.objects.filter(status="p", archived=False)
    serializer_class = DiagramSerializer


class TechnologyList(viewsets.ModelViewSet):
    serializer_class = TechnologySerializer
    queryset = Technology.objects.filter(status="p", archived=False)


class TrainingTermsList(viewsets.ModelViewSet):
    serializer_class = TrainingTermsSerializer
    queryset = TrainingTerms.objects.all()


class SemesterList(viewsets.ModelViewSet):
    serializer_class = SemesterSerializer
    queryset = Semester.objects.all()


class VariantList(viewsets.ModelViewSet):
    serializer_class = VariantSerializer
    queryset = Variant.objects.filter(status="p", archived=False)


#### DETAILS ####

class VariantDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Variant


class SemesterDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Semester


class TrainingTermsDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TrainingTerms


class TechnologyDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Technology


class DiagramDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Diagram


class ProgramDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Program


class ModuleDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Module


class TypeDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Type


class DisciplineDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Discipline


class ResultDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Result


class CompetenceDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Competence


class PersonDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person


class CourseDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course


class UserDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User


class TrainingTargetDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TrainingTarget


class ProgramCompetenceDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProgramCompetence


class TargetModulesDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TargetModules


class ChoiceGroupDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChoiceGroup


class ChoiceGroupTypeDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChoiceGroupType


@api_view(('GET',))
def get_choice_groups_by_program(request, program_id):
    response = []
    for cg in ChoiceGroup.objects.filter(program__id=program_id).order_by("number"):
        response.append({
            "id": cg.id,
            "title": cg.title,
            "get_choice_group_type_display": cg.get_choice_group_type_display(),
            "get_program_modules": cg.get_program_modules(),
            "number": cg.number,
            "labor": cg.labor,
            "program": cg.program.id,
        })
    return Response(response)


@api_view(('GET',))
def get_targets_by_program(request, program_id):
    response = []
    for target in TrainingTarget.objects.filter(program__id=program_id).order_by("number"):
        response.append({
            "id": target.id,
            "title": target.title,
            "number": target.number,
            "program": target.program.id,
        })
    return Response(response)


@api_view(('GET',))
def get_competences_by_program(request, program_id):
    response = [{"id": c.id,
                 "title": c.title,
                 "number": c.number,
                 } for c in ProgramCompetence.objects.filter(program__id=program_id)]
    return Response(sorted(response, key=lambda k: k['number']))


@api_view(('GET',))
def get_program_modules(request, program_id):
    trigger = Changed.objects.filter(program__id=program_id).first()
    if not trigger:
        trigger = Changed.objects.create(program=Program.objects.get(id=program_id))
        trigger.activate()
        trigger.save()
    if not trigger.state():
        return Response(cache.get(f"gpm-{program_id}"))
    response = []
    for mod in ProgramModules.objects.filter(program__id=program_id, status="p", archived=False):
        response.append({
                    "id": mod.id,
                    "title": mod.module.title,
                    "competence": None if not mod.competence else mod.competence.id,
                    "semester": 0 if not mod.semester else mod.semester,
                    "get_labor": mod.module.get_labor(),
                    "choice_group": None if not mod.choice_group else mod.choice_group.id,
                    "targets_positions": mod.get_target_positions(),
                    "priority": 9999 if not mod.module.uni_priority else mod.module.uni_priority
                    })
    response = sorted(response, key=lambda k: (k["semester"], k["priority"], k["title"]))
    cache.set(f"gpm-{program_id}", response, 2678400)
    trigger.deactivate()
    trigger.save()
    return Response(response)


@api_view(("POST", ))
def change_target_module(request):
    module_id = request.data["module_id"]
    target_id = request.data["target_id"]
    status = request.data["status"]

    program_module = ProgramModules.objects.get(id=module_id)
    target = TrainingTarget.objects.get(id=target_id)
    status = int(status)
    trigger = Changed.objects.filter(program=program_module.program).first()
    if not trigger:
        trigger = Changed.objects.create(program=program_module.program)
    if status == 0:
        tm = TargetModules.objects.filter(target=target, program_module=program_module).first()
        if tm:
            tm.delete()
    elif status == 1:
        tm = TargetModules.objects.filter(target=target, program_module=program_module).first()
        if tm:
            tm.choice_group = False
            tm.status = "p"
            tm.save()
        else:
            tm = TargetModules(target=target, program_module=program_module, choice_group=False)
            tm.status = "p"
            tm.save()
    elif status == 2:
        tm = TargetModules.objects.filter(target=target, program_module=program_module).first()
        if tm:
            tm.choice_group = True
            tm.status = "p"
            tm.save()
        else:
            tm = TargetModules(target=target, program_module=program_module, choice_group=True)
            tm.status = "p"
            tm.save()
    trigger.activate()
    return Response(status=200)


@api_view(("POST", ))
def change_choice_group(request):
    module_id = request.data["module_id"]
    choice_group_id = request.data["choice_group_id"]
    program_module = ProgramModules.objects.get(id=module_id)

    trigger = Changed.objects.filter(program=program_module.program).first()
    if not trigger:
        trigger = Changed.objects.create(program=program_module.program)

    if choice_group_id:
        chg = ChoiceGroup.objects.get(id=choice_group_id)
        program_module.choice_group = chg
    else:
        program_module.choice_group = None
    program_module.save()
    trigger.activate()
    return Response(status=200)


@api_view(("POST", ))
def change_competence(request):
    module_id = request.data["module_id"]
    competence_id = request.data["competence_id"]
    program_module = ProgramModules.objects.get(id=module_id)

    trigger = Changed.objects.filter(program=program_module.program).first()
    if not trigger:
        trigger = Changed.objects.create(program=program_module.program)

    if competence_id:
        comp = ProgramCompetence.objects.get(id=competence_id)
        program_module.competence = comp
    else:
        program_module.competence = None
    program_module.save()
    trigger.activate()
    return Response(status=200)


@api_view(("GET", ))
def heartbeat(request):
    return Response(status=200)


@api_view(('GET',))
def get_program_disciplines(request, program_id):
    response = []
    disciplines = (Discipline.objects.filter(module__id__in=[mod.module.id for mod in ProgramModules.objects.filter(program__id=program_id, status="p", archived=False)], status="p", archived=False))
    for discipline in disciplines:
        terms = {}
        for term in TrainingTerms.objects.all().order_by("title"):
            semesters = [s.training_semester for s in Semester.objects.filter(discipline=discipline, term=term, program=program_id)]
            terms[term.title] = 0 if len(semesters) == 0 else min(semesters)

        response.append({
                    "id": discipline.id,
                    "title": discipline.title,
                    "module": discipline.module.title,
                    "labor": discipline.labor,
                    "period": discipline.period,
                    "terms": terms,
                    "priority": 9999 if not discipline.module.uni_priority else discipline.module.uni_priority

                    })
    return Response(sorted(response, key=lambda k: (k["priority"], k["title"])))


@api_view(('POST',))
def change_discipline_semester(request):
    program = Program.objects.get(id=request.data["program_id"])
    discipline = Discipline.objects.get(id=request.data["discipline_id"])
    term_title = request.data["term_title"]
    new_semester = request.data["semester"]

    semester = Semester.objects.filter(program=program, discipline=discipline, term__title=term_title)
    if semester:
        semester.update(training_semester=new_semester, year=date.today().year)
    else:
        Semester.objects.create(program=program, discipline=discipline, term=TrainingTerms.objects.filter(title=term_title).first(), training_semester=new_semester, year=date.today().year)
    return Response(status=200)


@api_view(('GET',))
def get_variants(request, program_id, discipline_id):
    variants = Variant.objects.filter(program__id=program_id, discipline__id=discipline_id)
    return Response([{
                    "id": variant.id,
                    "diagram": None if not variant.diagram else
                    {
                        "id": variant.diagram.id,
                        "title": variant.diagram.title,
                        "diagram": variant.diagram.diagram
                    },
                    "course": None if not variant.course else
                    {
                        "title": variant.course.title
                    },
                    "technology": None if not variant.technology else
                    {
                        "id": variant.technology.id,
                        "title": variant.technology.title,
                        "description": variant.technology.description,
                        "contact_work_category": variant.technology.contact_work_category,
                        "color": variant.technology.color
                    },
                    "semester": None if not variant.semester else
                    {
                        "id": variant.semester,
                        "term": variant.semester.term.title,
                        "training_semester": variant.semester.training_semester,
                    },
                    "parity": None if not variant.parity else variant.parity,
                    "link": variant.link
                     } for variant in variants])


@api_view(('POST',))
def change_variant(request):
    variant = get_object_or_404(Variant, pk=request.data["variant_id"])
    for key, value in request.data.items():
        if key != "variant_id":
            value = request.data.get(key, None)
            if value:
                variant.__dict__[key] = value
            else:
                variant.__dict__[key] = None

    variant.status = "p"
    variant.save()
    return Response(status=200)


@api_view(('POST',))
def create_variant(request):
    program = Program.objects.get(id=request.data["program_id"])
    discipline = Discipline.objects.get(id=request.data["discipline_id"])
    term_title = request.data.get("term_title", None)

    technology = request.data.get("technology_id", None)
    diagram = request.data.get("diagram_id", None)
    course = request.data.get("course_id", None)
    parity = request.data.get("parity_id", None)
    link = request.data.get("link", None)

    if term_title:
        semester = Semester.objects.filter(program=program, discipline=discipline, term__title=term_title).first()
        Variant.objects.create(discipline=discipline, program=program, semester=semester, technology=technology,
                               diagram=diagram, link=link, status="p")
    elif course:
        Variant.objects.create(discipline=discipline, program=program, technology=technology,
                               course=Course.objects.get(id=course), diagram=diagram, link=link, status="p")
    elif parity:
        Variant.objects.create(discipline=discipline, program=program, parity=parity, technology=technology,
                               diagram=diagram, link=link, status="p")
    return Response(status=200)


@api_view(('GET',))
def get_program_variants(request, program_id):
    variants = {}
    program = Program.objects.get(id=program_id)
    disciplines = program.get_all_disciplines()
    for discipline in disciplines:
        variants[discipline.id] = []
        for variant in Variant.objects.filter(program=program, discipline__id=discipline.id):
            variants[discipline.id].append(
                {
                    "id": variant.id,
                    "diagram": None if not variant.diagram else
                    {
                        "id": variant.diagram.id,
                        "title": variant.diagram.title,
                        "diagram": variant.diagram.diagram
                    },
                    "course": None if not variant.course else
                    {
                        "title": variant.course.title
                    },
                    "technology": None if not variant.technology else
                    {
                        "id": variant.technology.id,
                        "title": variant.technology.title,
                        "description": variant.technology.description,
                        "contact_work_category": variant.technology.contact_work_category,
                        "color": variant.technology.color
                    },
                    "semester": None if not variant.semester else
                    {
                        "id": variant.semester,
                        "term": variant.semester.term.title,
                        "training_semester": variant.semester.training_semester,
                    },
                    "parity": None if not variant.parity else variant.parity,
                    "link": variant.link
                }
            )
    return Response(variants)


@api_view(('POST',))
def delete_variant(request):
    variant = get_object_or_404(Variant, pk=request.data["variant_id"])
    variant.delete()
    return Response(status=200)
