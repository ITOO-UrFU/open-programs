from rest_framework import viewsets
from rest_framework import serializers

from django.contrib.auth.models import User
from courses.models import Course, Session
from persons.models import Person
from competences.models import Competence
from results.models import Result
from disciplines.models import Discipline
from modules.models import Module, Type, GeneralBaseModulesPool, EducationalProgramTrajectoriesPool, ChoiceModulesPool

from courses.serializers import CourseSerializer, SessionSerializer
from persons.serializers import UserSerializer, PersonSerializer
from competences.serializers import CompetenceSerializer
from results.serializers import ResultSerializer
from disciplines.serializers import DisciplineSerializer
from modules.serializers import ModuleSerializer, TypeSerializer, GeneralBaseModulesPoolSerializer, \
    EducationalProgramTrajectoriesPoolSerializer, ChoiceModulesPoolSerializer


class PersonList(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class UserList(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CourseList(viewsets.ModelViewSet):
    queryset = Course.objects.filter(status="p", archived=False)
    serializer_class = CourseSerializer


class SessionList(viewsets.ModelViewSet):
    queryset = Session.objects.filter(status="p", archived=False)
    serializer_class = SessionSerializer


class CompetenceList(viewsets.ModelViewSet):
    queryset = Competence.objects.filter(status="p", archived=False)
    serializer_class = CompetenceSerializer


class ResultList(viewsets.ModelViewSet):
    queryset = Result.objects.filter(status="p", archived=False)
    serializer_class = ResultSerializer


class DisciplineList(viewsets.ModelViewSet):
    queryset = Discipline.objects.filter(status="p", archived=False)
    serializer_class = DisciplineSerializer


class ModuleList(viewsets.ModelViewSet):
    queryset = Module.objects.filter(status="p", archived=False)
    serializer_class = ModuleSerializer


class TypeList(viewsets.ModelViewSet):
    queryset = Type.objects.filter(status="p", archived=False)
    serializer_class = TypeSerializer


class GeneralBaseModulesPoolList(viewsets.ModelViewSet):
    queryset = GeneralBaseModulesPool.objects.filter(status="p", archived=False)
    serializer_class = GeneralBaseModulesPoolSerializer


class EducationalProgramTrajectoriesPoolList(viewsets.ModelViewSet):
    queryset = EducationalProgramTrajectoriesPool.objects.filter(status="p", archived=False)
    serializer_class = EducationalProgramTrajectoriesPoolSerializer


class ChoiceModulesPoolList(viewsets.ModelViewSet):
    queryset = ChoiceModulesPool.objects.filter(status="p", archived=False)
    serializer_class = ChoiceModulesPoolSerializer


class ModuleDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Module


class TypeDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Type


class GeneralBaseModulesPoolDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GeneralBaseModulesPool


class EducationalProgramTrajectoriesPoolDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EducationalProgramTrajectoriesPool


class ChoiceModulesPoolDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChoiceModulesPool


class DisciplineDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Discipline


class ResultDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Result


class CompetenceDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Competence


class CourseDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course


class SessionDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Session


class PersonDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person


class UserDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User