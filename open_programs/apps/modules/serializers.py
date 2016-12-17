from .models import Type, Module, GeneralBaseModulesPool, EducationalProgramTrajectoriesPool, ChoiceModulesPool
from disciplines.models import Discipline
from disciplines.serializers import DisciplineSerializer
from rest_framework import serializers


class TypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Type
        fields = ("title", "description", "status", "archived", "created", "updated")


class ModuleSerializer(serializers.HyperlinkedModelSerializer):

    type = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=True,
    )

    disciplines = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,

    )

    class Meta:
        model = Module
        fields = ("id", "title", "description", "disciplines", "type", "results", "results_text", "competences", "status", "archived", "created", "updated")


class GeneralBaseModulesPoolSerializer(serializers.HyperlinkedModelSerializer):

    modules = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )

    class Meta:
        model = GeneralBaseModulesPool
        fields = ("id", "title", "description", "modules", "status", "archived", "created", "updated")


class EducationalProgramTrajectoriesPoolSerializer(serializers.HyperlinkedModelSerializer):

    modules = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )

    class Meta:
        model = EducationalProgramTrajectoriesPool
        fields = ("id", "title", "description", "modules", "status", "archived", "created", "updated")


class ChoiceModulesPoolSerializer(serializers.HyperlinkedModelSerializer):

    modules = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )

    class Meta:
        model = ChoiceModulesPool
        fields = ("id", "title", "description", "modules", "status", "archived", "created", "updated")
