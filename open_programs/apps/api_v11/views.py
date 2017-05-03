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
                 } for c in ProgramCompetence.objects.filter(program__id=program_id)]
    return Response(response)


@api_view(('GET',))
def get_program_modules(request, program_id):
    response = []
    for cg in ChoiceGroup.objects.filter(program__id=program_id).order_by("number"):
        tmp = []
        mods = [program_module.module.id for program_module in ProgramModules.objects.filter(program=Program.objects.get(pk=program_id), choice_group=cg, status="p", archived=False)]

        for mod in Module.objects.filter(pk__in=mods):
            pr_mod = ProgramModules.objects.filter(program=Program.objects.get(pk=program_id), choice_group=cg, module=mod, status="p", archived=False).first()

            targets_positions = []
            try:
                tr_targets = TrainingTarget.objects.filter(program__id=program_id).order_by('number')
                for tt in tr_targets:
                    tms = TargetModules.objects.filter(program_module=pr_mod, target=tt, status="p",
                                                       archived=False)
                    if not tms:
                        status = 0
                    for target_module in tms:
                        if target_module.choice_group is False:
                            status = 1
                        elif target_module.choice_group is True:
                            status = 2
                    targets_positions.append(status)

            except:
                pass

            disciplines_semesters = Discipline.objects.filter(pk__in=mod.get_all_discipline_ids()).values("period")
            try:
                first_semester = max([ds["period"] for ds in disciplines_semesters])
                weight = first_semester + pr_mod.semester
            except:
                weight = pr_mod.semester

            try:
                competence_id = pr_mod.competence.id
            except:
                competence_id = None


            response.append({
                "id": pr_mod.id,
                "title": mod.title,
                "description": mod.description,
                "competence": competence_id,
                "semester": pr_mod.semester,
                "weight": weight,
                "get_all_discipline_ids": mod.get_all_discipline_ids(),
                # "get_all_disciplines": mod.get_all_disciplines(),
                "get_type_display": mod.get_type_display(),
                # "results": mod.results,
                "results_text": mod.results_text,
                # "competences": mod.competences,
                "get_labor": mod.get_labor(),
                "choice_group": cg.id,
                "targets_positions": targets_positions,
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
    chg = ChoiceGroup.objects.get(id=choice_group_id)
    program_module.choice_group = chg
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
