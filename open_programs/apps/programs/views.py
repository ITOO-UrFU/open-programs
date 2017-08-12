from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Program, TrainingTarget, ProgramModules, ChoiceGroup, ProgramCompetence
from disciplines.models import Discipline


class ProgramBackup(APIView):
    def get(self, request, id):
        program = Program.objects.get(id=id)
        targets = TrainingTarget.objects.filter(program=program)
        pms = ProgramModules.objects.filter(program=program)
        cgs = ChoiceGroup.objects.filter(program=program)
        comps = ProgramCompetence.objects.filter(program=program)

        response = []
        for pm in pms:
            disciplines = []
            for d in Discipline.objects.filter(module=pm.module, status="p",archived=False):
                disciplines.append({
                    "title": d.title
                })
            response.append({
                "module": pm.module.uni_number,
                "choice_group": None if not pm.choice_group else pm.choice_group.title,
                "choice_group_type": None if not pm.choice_group else pm.choice_group.get_choice_group_type_display(),
                "competence": None if not pm.competence else pm.competence.title,
                "semester": pm.semester,
                "index": pm.index,
                "disciplines": disciplines
            })

        return Response(response)
