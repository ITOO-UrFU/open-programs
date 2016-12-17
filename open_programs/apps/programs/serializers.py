from .models import Program
from modules.models import Module
from rest_framework import serializers


class ProgramSerializer(serializers.HyperlinkedModelSerializer):
    chief = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=True,
    )

    modules = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=False,
        view_name='module-detail',
        queryset=Module.objects.all(),
        lookup_field="title"
    )

    class Meta:
        model = Program
        fields = ("id", "title", "chief", "modules", "status", "archived", "created", "updated")