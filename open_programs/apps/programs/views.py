from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Program, TrainingTarget, ProgramModules, ChoiceGroup, ProgramCompetence


class ProgramCompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramCompetence
        fields = ("id", "title", "number")


class ChoiceGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoiceGroup
        fields = ("id", "title", "labor", "get_choice_group_type_display", "number")


class ProgramModulesSerializer(serializers.ModelSerializer):
    choice_group = ChoiceGroupSerializer
    competence = ProgramCompetenceSerializer

    class Meta:
        model = ProgramModules
        fields = ("id", "module__uni_number", "choice_group", "competence", "semester", "index")


class ProgramBackup(APIView):
    def get(self, request, id):
        program = Program.objects.get(id=id)
        targets = TrainingTarget.objects.filter(program=program)
        pms = ProgramModules.objects.filter(program=program)
        cgs = ChoiceGroup.objects.filter(program=program)
        comps = ProgramCompetence.objects.filter(program=program)

        serializer = ProgramModulesSerializer(pms)

        return Response(serializer.data)
