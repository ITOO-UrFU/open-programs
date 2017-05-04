from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView

from django.contrib.auth.models import User
from courses.models import Course, Session
from persons.models import Person
from competences.models import Competence
from results.models import Result
from disciplines.models import Discipline
from modules.models import Module, Type
from programs.models import Program, TrainingTarget, ProgramCompetence, ProgramModules, \
                            TargetModules, ChoiceGroup, ChoiceGroupType

from courses.serializers import CourseSerializer, SessionSerializer, CourseIdSerializer
from persons.serializers import UserSerializer, PersonSerializer
from competences.serializers import CompetenceSerializer
from results.serializers import ResultSerializer
from modules.serializers import ModuleSerializer, TypeSerializer
from programs.serializers import ProgramSerializer, TrainingTargetSerializer, \
                                 ProgramCompetenceSerializer, ChoiceGroupTypeSerializer, \
                                 ChoiceGroupSerializer, ProgramModulesSerializer, TargetModulesSerializer
from disciplines.serializers import DisciplineSerializer

from cms.api_views import *


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

#### DETAILS ####


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
    response = []
    for mod in ProgramModules.objects.filter(program__id=program_id, status="p", archived=False):

        response.append({
                    "id": mod.id,
                    "title": mod.module.title,
                    "description": mod.module.description,
                    "competence": None if not mod.competence else mod.competence.id,
                    "semester": mod.semester,
                    "weight": mod.get_weight(),
                    "get_all_discipline_ids": mod.module.get_all_discipline_ids(),
                    "get_type_display": mod.module.get_type_display(),
                    "results_text": mod.module.results_text,
                    "get_labor": mod.module.get_labor(),
                    "choice_group": None if not mod.choice_group else mod.choice_group.id,
                    "targets_positions": mod.get_target_positions(),
                    })
    return Response(sorted(response, key=lambda k: k['weight']))


@api_view(("POST", ))
def change_target_module(request):
    module_id = request.data["module_id"]
    target_id = request.data["target_id"]
    status = request.data["status"]

    program_module = ProgramModules.objects.get(id=module_id)
    target = TrainingTarget.objects.get(id=target_id)
    status = int(status)
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
    return Response(status=200)


@api_view(("POST", ))
def change_choice_group(request):
    module_id = request.data["module_id"]
    choice_group_id = request.data["choice_group_id"]

    program_module = ProgramModules.objects.get(id=module_id)

    if choice_group_id:
        chg = ChoiceGroup.objects.get(id=choice_group_id)
        program_module.choice_group = chg
    else:
        program_module.choice_group = None
    program_module.save()
    return Response(status=200)


@api_view(("POST", ))
def change_competence(request):
    module_id = request.data["module_id"]
    competence_id = request.data["competence_id"]

    program_module = ProgramModules.objects.get(id=module_id)
    if competence_id:
        comp = ProgramCompetence.objects.get(id=competence_id)
        program_module.competence = comp
    else:
        program_module.competence = None
    program_module.save()
    return Response(status=200)


@api_view(("GET", ))
def heartbeat(request):
    return Response(status=200)
