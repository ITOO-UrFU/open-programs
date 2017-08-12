from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Program, TrainingTarget


class ProgramBackup(APIView):

    def get(self, request, id):
        program = Program.objects.get(td=id)
        targets = TrainingTarget.objects.filter(program=program)
        return Response([target.title for target in targets])
