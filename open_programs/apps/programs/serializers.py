from .models import Program
from rest_framework import serializers


class ProgramSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Program
        fields = ("id", "title", "chief", "general_base_modules", "educational_program_trajectories", "choice_modules", "status", "archived", "created", "updated")