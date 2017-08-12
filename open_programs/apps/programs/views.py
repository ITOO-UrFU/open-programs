from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Program, TrainingTarget, ProgramModules, ChoiceGroup, ProgramCompetence
from disciplines.models import Discipline, Semester, TrainingTerms, Diagram, Technology, Variant


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
            for d in Discipline.objects.filter(module=pm.module, status="p", archived=False).iterator():
                variants = []
                for v in Variant.objects.filter(discipline=d, program=program).iterator():
                    variants.append({
                        "course": None if not v.course else {
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
