from .models import Program
from modules.serializers import ModuleSerializer, EducationalProgramTrajectoriesPoolSerializer, ChoiceModulesPoolSerializer
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

    # educational_program_trajectories = EducationalProgramTrajectoriesPoolSerializer(
    #     many=True,
    #     read_only=False,
    # )
    #
    # choice_modules = ChoiceModulesPoolSerializer(
    #     many=True,
    #     read_only=False,
    # )

    class Meta:
        model = Program
        fields = ("id", "title", "chief", "modules", "module_dependencies", "status", "archived", "created", "updated")
        # "educational_program_trajectories", "choice_modules",