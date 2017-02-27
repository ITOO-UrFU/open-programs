from rest_framework import viewsets
from rest_framework import serializers

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


class ProgramModulesDetail(serializers.HyperlinkedModelSerializer):
    module = ModuleSerializer

    class Meta:
        model = ProgramModules
        fields =("id", "program", "module", "choice_group", "competence", "period_start", "period_end")


class ChoiceGroupDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChoiceGroup


class ChoiceGroupTypeDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChoiceGroupType

