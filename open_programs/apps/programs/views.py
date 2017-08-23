import json

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Program, TrainingTarget, ProgramModules, ChoiceGroup, ProgramCompetence
from .models import ProgramBackup as PB
from disciplines.models import Discipline, Semester, TrainingTerms, Diagram, Technology, Variant


class ProgramBackup(APIView):
    @staticmethod
    def get(request, id):
        program = Program.objects.get(id=id)
        targets = TrainingTarget.objects.filter(program=program)
        pms = ProgramModules.objects.filter(program=program)
        cgs = ChoiceGroup.objects.filter(program=program)
        comps = ProgramCompetence.objects.filter(program=program)

        modules = []
        for pm in pms:
            disciplines = []
            for d in Discipline.objects.filter(module=pm.module, status="p", archived=False).iterator():
                variants = []
                for v in Variant.objects.filter(discipline=d, program=program).iterator():
                    variants.append({
                        "course": None if not v.course else {
                            "id": v.course.id,
                            "title": v.course.title,
                        },
                        "semester": None if not v.semester else {
                            "training_semester": v.semester.training_semester,
                            "term": v.semester.term.title,
                        },
                        "parity": v.parity,
                        "link": v.link,
                        "diagram": None if not v.diagram else v.diagram.title,
                    })
                terms = {}
                for term in TrainingTerms.objects.all().order_by("title"):
                    semesters = [s.training_semester for s in
                                 Semester.objects.filter(discipline=d, term=term, program=program)]
                    terms[term.title] = 0 if len(semesters) == 0 else min(semesters)

                disciplines.append({
                    "title": d.title,
                    "labor": d.labor,
                    "period": d.period,
                    "terms": terms,
                    "priority": None if not d.module.uni_priority else d.module.uni_priority,
                    "variants": variants,
                })
            modules.append({
                "module": pm.module.uni_number,
                "choice_group": None if not pm.choice_group else pm.choice_group.title,
                "choice_group_type": None if not pm.choice_group else pm.choice_group.get_choice_group_type_display(),
                "competence": None if not pm.competence else pm.competence.title,
                "semester": pm.semester,
                "index": pm.index,
                "disciplines": disciplines
            })

            response = {
                "program": program.title,
                "choice_groups": [cg.title for cg in cgs],
                "competences": [c.title for c in comps],
                "targets": [t.title for t in targets],
                "modules": modules,

            }
        pb = PB(title=program.title, json=response, status="p")
        pb.save()
        return Response(response)


class RestoreBackup(APIView):
    @staticmethod
    def get(request, id):
        pb = PB.objects.get(pk=id)
        data = pb.json
        program = Program.objects.filter(title=data["program"], archived=False).first()

        #Restore choice groups
        for cgb in data["choice_groups"]:
            cg = ChoiceGroup.objects.filter(title=cgb, program=program).exists()
            if not cg:
                print(f"Need create CG {cgb}")
                ChoiceGroup.objects.create(title=cgb, program=program, status="p")


