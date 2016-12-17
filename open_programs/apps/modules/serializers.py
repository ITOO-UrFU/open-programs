from .models import Type, Module, GeneralBaseModulesPool, EducationalProgramTrajectoriesPool, ChoiceModulesPool
from disciplines.models import Discipline
from disciplines.serializers import DisciplineSerializer
from rest_framework import serializers


class TypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Type
        fields = ("title", "description", "status", "archived", "created", "updated")


class ModuleSerializer(serializers.HyperlinkedModelSerializer):

    type = TypeSerializer(
        many=False,
        read_only=False,
        # view_name='discipline-detail',
        # queryset=Discipline.objects.all(),
        # lookup_field="name"
    )

    disciplines = DisciplineSerializer(
        many=True,
        read_only=True,
        # view_name='discipline-detail',
        # queryset=Discipline.objects.all(),
        # lookup_field="name"
    )

    class Meta:
        model = Module
        fields = ("id", "title", "description", "disciplines", "type", "results", "results_text", "competences", "status", "archived", "created", "updated")


class GeneralBaseModulesPoolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GeneralBaseModulesPool
        fields = ("id", "title", "description", "modules", "status", "archived", "created", "updated")


class EducationalProgramTrajectoriesPoolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EducationalProgramTrajectoriesPool
        fields = ("id", "title", "description", "modules", "status", "archived", "created", "updated")


class ChoiceModulesPoolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChoiceModulesPool
        fields = ("id", "title", "description", "modules", "status", "archived", "created", "updated")
