from .models import Program
from modules.serializers import ModuleSerializer
from persons.serializers import PersonSerializer

from rest_framework import serializers


class ProgramSerializer(serializers.HyperlinkedModelSerializer):
    chief = PersonSerializer(
        many=False,
        read_only=False,
    )

    modules = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Program
        fields = ("id", "title", "chief", "modules", "module_dependencies", "status", "archived", "created", "updated")
