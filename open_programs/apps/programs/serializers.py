from .models import Program, TrainingTarget, ProgramCompetence, ProgramModules, TargetModules, ChoiceGroup, ChoiceGroupType
from persons.serializers import PersonSerializer
from modules.serializers import ModuleSerializer

from rest_framework import serializers


class ProgramCompetenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProgramCompetence
        fields = ("id", "title", "number")


class ProgramSerializer(serializers.ModelSerializer):
    chief = PersonSerializer(
        many=False,
        read_only=False,
    )

    class Meta:
        model = Program
        fields = ("id", "title", "chief", "get_level_display", "get_choice_groups", "training_direction", "competences")


class TrainingTargetSerializer(serializers.ModelSerializer):
    program = ProgramSerializer

    class Meta:
        model = TrainingTarget
        fields = ("id", "title", "program", "number")


class ChoiceGroupTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoiceGroupType
        fields = ("id", "title")


class ChoiceGroupSerializer(serializers.ModelSerializer):
    program = ProgramSerializer

    class Meta:
        model = ChoiceGroup
        fields = ("id", "program", "title", "labor", "get_choice_group_type_display", "get_program_modules", "number")


class ProgramModulesSerializer(serializers.ModelSerializer):
    program = ProgramSerializer
    module = ModuleSerializer
    choice_group = ChoiceGroupSerializer
    competence = ProgramCompetenceSerializer

    class Meta:
        model = ProgramModules
        fields = ("id", "program", "module", "choice_group", "get_competence_display", "semester")


class TargetModulesSerializer(serializers.ModelSerializer):
    target = TrainingTargetSerializer
    program_module = ProgramModulesSerializer
    choice_group = ChoiceGroupSerializer

    class Meta:
        model = TargetModules
        fields = ("id", "target", "program_module", "choice_group")
