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
    competence = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='title'
    )
    choice_group = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='title'
    )
    module = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='uni_number'
    )

    class Meta:
        model = ProgramModules
        fields = ("module", "choice_group", "competence", "semester", "index")


class ProgramBackup(APIView):
    def get(self, request, id):
        program = Program.objects.get(id=id)
        targets = TrainingTarget.objects.filter(program=program)
        pms = ProgramModules.objects.filter(program=program)
        cgs = ChoiceGroup.objects.filter(program=program)
        comps = ProgramCompetence.objects.filter(program=program)

        response = []
        for pm in pms:
            response.append({
                "module": pm.module.uni_number,
                "choice_group": None if not pm.choice_group else pm.choice_group.title,
                "choice_group_type": None if not pm.choice_group else pm.choice_group.get_choice_group_type_display,
                "competence": None if not pm.competence else pm.competence.title,
                "semester": pm.semester,
                "index": pm.index
            })

        return Response(response)
