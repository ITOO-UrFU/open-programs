from .models import Type, Module
from disciplines.serializers import DisciplineSerializer
from rest_framework import serializers


class TypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Type
        fields = ("title", "description", "status", "archived", "created", "updated")


class ModuleSerializer(serializers.HyperlinkedModelSerializer):

    get_all_disciplines = DisciplineSerializer(
        many=True,
    )

    class Meta:
        model = Module
        fields = ("id", "title", "description", "get_all_disciplines", "get_type_display", "results", "results_text", "competences", "get_labor")
