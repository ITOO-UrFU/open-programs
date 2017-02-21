from .models import Type, Module
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

    get_all_disciplines = DisciplineSerializer(
        many=True,
    )

    class Meta:
        model = Module
        fields = ("id", "title", "description", "get_all_disciplines", "type", "results", "results_text", "competences")
