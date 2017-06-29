from datetime import date
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.generics import ListCreateAPIView, CreateAPIView


from rest_framework_extensions.cache.mixins import CacheResponseMixin

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from courses.models import Course, Session
from persons.models import Person
from competences.models import Competence
from results.models import Result
from disciplines.models import Discipline, Semester, TrainingTerms, Diagram, Technology, Variant
from modules.models import Module, Type
from programs.models import Program, TrainingTarget, ProgramCompetence, ProgramModules, \
                            TargetModules, ChoiceGroup, ChoiceGroupType, Changed, StudentProgram

from courses.serializers import CourseSerializer, SessionSerializer, CourseIdSerializer
from persons.serializers import UserSerializer, PersonSerializer
from competences.serializers import CompetenceSerializer
from results.serializers import ResultSerializer
from modules.serializers import ModuleSerializer, TypeSerializer
from programs.serializers import ProgramSerializer, TrainingTargetSerializer, \
                                 ProgramCompetenceSerializer, ChoiceGroupTypeSerializer, \
                                 ChoiceGroupSerializer, ProgramModulesSerializer, TargetModulesSerializer
from disciplines.serializers import *

from cms.api_views import *

from django.core.cache import cache

from functools import wraps
from django.http import HttpResponseForbidden
from django.utils.decorators import available_attrs
import logging

def is_manager(f):
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            logging.critical(request.user)
            print(request.user, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            if not request.user.groups.filter(name__in=['manager']).exists():
                pass #return HttpResponseForbidden(f)
            return func(request, *args, **kwargs)
        return inner
    return decorator



class ProgramList(CacheResponseMixin, viewsets.ModelViewSet):
    queryset = Program.objects.filter(status="p", archived=False)
    serializer_class = ProgramSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        # print(queryset, "!!!!!!!!!!!!!!!!!!!")
        # if filter_kwargs["pk"]:
        #     print(filter_kwargs["pk"], '!!!!!!!!!!!!!!')

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj


class ModuleList(viewsets.ModelViewSet):
    queryset = Module.objects.filter(status="p", archived=False)
    serializer_class = ModuleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)


class TypeList(viewsets.ModelViewSet):
    queryset = Type.objects.filter(status="p", archived=False)
    serializer_class = TypeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)


class DisciplineList(viewsets.ModelViewSet):
    queryset = Discipline.objects.filter(archived=False)
    serializer_class = DisciplineSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)


class ResultList(viewsets.ModelViewSet):
    queryset = Result.objects.filter(status="p", archived=False)
    serializer_class = ResultSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)


class CompetenceList(viewsets.ModelViewSet):
    queryset = Competence.objects.filter(status="p", archived=False)
    serializer_class = CompetenceSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)


# class CompetenceListCreateView(ListCreateAPIView):
#     model = Competence
#     serializer_class = CompetenceSerializer
#     @classmethod
#     def create(cls, request, *args, **kwargs):
#         data = request.DATA
#
#         c = Competence.objects.create(title=data["title"], status="p",results=Result.objects.get)
#
#         # ... create nested objects from request data ...
#
#         # ...
#         return Response(serializer.data,
#                         status=status.HTTP_201_CREATED,
#                         headers=headers)


class PersonList(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class CourseList(viewsets.ModelViewSet): ##CacheResponseMixin,
    queryset = Course.objects.filter(status="p", archived=False)
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)


class UserList(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TrainingTargetList(viewsets.ModelViewSet):
    queryset = TrainingTarget.objects.filter(status="p", archived=False)
    serializer_class = TrainingTargetSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)


class ProgramCompetenceList(CacheResponseMixin, viewsets.ModelViewSet):
    queryset = ProgramCompetence.objects.filter(status="p", archived=False)
    serializer_class = ProgramCompetenceSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)


class ProgramModulesList(CacheResponseMixin, viewsets.ModelViewSet):
    queryset = ProgramModules.objects.filter(status="p", archived=False)
    serializer_class = ProgramModulesSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)


class TargetModulesList(viewsets.ModelViewSet):
    queryset = TargetModules.objects.filter(status="p", archived=False)
    serializer_class = TargetModulesSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)


class ChoiceGroupList(viewsets.ModelViewSet):
    queryset = ChoiceGroup.objects.filter(status="p", archived=False)
    serializer_class = ChoiceGroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)


class ChoiceGroupTypeList(viewsets.ModelViewSet):
    queryset = ChoiceGroupType.objects.filter(status="p", archived=False)
    serializer_class = ChoiceGroupTypeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)


class DiagramList(viewsets.ModelViewSet):
    queryset = Diagram.objects.filter(status="p", archived=False)
    serializer_class = DiagramSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)


class TechnologyList(viewsets.ModelViewSet):
    serializer_class = TechnologySerializer
    queryset = Technology.objects.filter(status="p", archived=False)
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)


class TrainingTermsList(viewsets.ModelViewSet):
    serializer_class = TrainingTermsSerializer
    queryset = TrainingTerms.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)


class SemesterList(viewsets.ModelViewSet):
    serializer_class = SemesterSerializer
    queryset = Semester.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)


class VariantList(viewsets.ModelViewSet):
    serializer_class = VariantSerializer
    queryset = Variant.objects.filter(status="p", archived=False)
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)


#### DETAILS ####

class VariantDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Variant


class SemesterDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Semester


class TrainingTermsDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TrainingTerms


class TechnologyDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Technology


class DiagramDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Diagram


class ProgramDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Program


class ModuleDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Module


class TypeDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Type


class DisciplineDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Discipline


class ResultDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Result


class CompetenceDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Competence


class PersonDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person


class CourseDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course


class UserDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User


class TrainingTargetDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TrainingTarget


class ProgramCompetenceDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProgramCompetence


class TargetModulesDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TargetModules


class ChoiceGroupDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChoiceGroup


class ChoiceGroupTypeDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChoiceGroupType


@api_view(('GET',))
@permission_classes((IsAuthenticatedOrReadOnly, ))
def get_choice_groups_by_program(request, program_id):
    response = []
    for cg in ChoiceGroup.objects.filter(program__id=program_id).order_by("number"):
        response.append({
            "id": cg.id,
            "title": cg.title,
            "get_choice_group_type_display": cg.get_choice_group_type_display(),
            "get_program_modules": cg.get_program_modules(),
            "number": cg.number,
            "labor": cg.labor,
            "program": cg.program.id,
        })
    return Response(response)


@api_view(('GET',))
@permission_classes((IsAuthenticatedOrReadOnly, ))
def get_targets_by_program(request, program_id):
    trigger = Changed.objects.filter(program__id=program_id, view="gpt").first()
    if not trigger:
        trigger = Changed.objects.create(program_id=program_id, view="gpt")
        trigger.activate()
        trigger.save()
    if not trigger.state():
        return Response(cache.get(f"gpt-{program_id}"))

    response = []
    program = Program.objects.get(id=program_id)

    for target in TrainingTarget.objects.filter(program=program).order_by("number"):
        choice_groups = []
        for cg in ChoiceGroup.objects.filter(program=program).order_by("number"):
            cgmodules = cg.get_program_modules()
            tm = TargetModules.objects.filter(target=target, program_module__in=cgmodules).count()
            if tm > 0:
                choice_groups.append(cg.id)
        response.append({
            "id": target.id,
            "title": target.title,
            "number": target.number,
            "program": target.program.id,
            "choice_groups": choice_groups,
        })
    cache.set(f"gpt-{program_id}", response, 2678400)
    trigger.deactivate()
    trigger.save()
    return Response(response)


@api_view(('GET',))
@permission_classes((IsAuthenticatedOrReadOnly, ))
def get_competences_by_program(request, program_id):
    response = [{"id": c.id,
                 "title": c.title,
                 "number": c.number,
                 } for c in ProgramCompetence.objects.filter(program__id=program_id)]
    return Response(sorted(response, key=lambda k: k['number']))


@api_view(('GET',))
@permission_classes((IsAuthenticatedOrReadOnly, ))
def get_program_modules(request, program_id):
    trigger = Changed.objects.filter(program__id=program_id, view="gpm").first()
    if not trigger:
        trigger = Changed.objects.create(program_id=program_id, view="gpm")
        trigger.activate()
        trigger.save()
    if not trigger.state():
        return Response(cache.get(f"gpm-{program_id}"))
    response = []
    for mod in ProgramModules.objects.filter(program__id=program_id, status="p", archived=False):
        response.append({
                    "id": mod.id,
                    "title": mod.module.title,
                    "competence": None if not mod.competence else mod.competence.id,
                    "semester": 0 if not mod.semester else mod.semester,
                    "get_labor": mod.module.get_labor(),
                    "choice_group": None if not mod.choice_group else mod.choice_group.id,
                    "targets_positions": mod.get_target_positions(),
                    "targets_positions_indexed": mod.get_target_positions_indexed(),
                    "priority": 9999 if not mod.module.uni_priority else mod.module.uni_priority,
                    "disciplines": mod.module.get_all_discipline_custom()
                    })
    response = sorted(response, key=lambda k: (k["semester"], k["priority"], k["title"]))
    cache.set(f"gpm-{program_id}", response, 2678400)
    trigger.deactivate()
    trigger.save()
    return Response(response)


@api_view(("POST", ))
@is_manager
def change_target_module(request):
    module_id = request.data["module_id"]
    target_id = request.data["target_id"]
    status = request.data["status"]

    program_module = ProgramModules.objects.get(id=module_id)
    target = TrainingTarget.objects.get(id=target_id)
    status = int(status)
    trigger = Changed.objects.filter(program=program_module.program, view="gpm").first()
    if not trigger:
        trigger = Changed.objects.create(program=program_module.program, view="gpm")
    if status == 0:
        tm = TargetModules.objects.filter(target=target, program_module=program_module).first()
        if tm:
            tm.delete()
    elif status == 1:
        tm = TargetModules.objects.filter(target=target, program_module=program_module).first()
        if tm:
            tm.choice_group = False
            tm.status = "p"
            tm.save()
        else:
            tm = TargetModules(target=target, program_module=program_module, choice_group=False)
            tm.status = "p"
            tm.save()
    elif status == 2:
        tm = TargetModules.objects.filter(target=target, program_module=program_module).first()
        if tm:
            tm.choice_group = True
            tm.status = "p"
            tm.save()
        else:
            tm = TargetModules(target=target, program_module=program_module, choice_group=True)
            tm.status = "p"
            tm.save()
    trigger.activate()
    return Response(status=200)


@api_view(("POST", ))
@is_manager
def change_choice_group(request):
    module_id = request.data["module_id"]
    choice_group_id = request.data["choice_group_id"]
    program_module = ProgramModules.objects.get(id=module_id)

    trigger = Changed.objects.filter(program=program_module.program, view="gpm").first()
    if not trigger:
        trigger = Changed.objects.create(program=program_module.program, view="gpm")

    if choice_group_id:
        chg = ChoiceGroup.objects.get(id=choice_group_id)
        program_module.choice_group = chg
    else:
        program_module.choice_group = None
    program_module.save()
    trigger.activate()
    return Response(status=200)


@api_view(("POST", ))
@permission_classes((DjangoModelPermissions, )) #
def change_competence(request):
    module_id = request.data["module_id"]
    competence_id = request.data["competence_id"]
    program_module = ProgramModules.objects.get(id=module_id)

    trigger = Changed.objects.filter(program=program_module.program, view="gpm").first()
    if not trigger:
        trigger = Changed.objects.create(program=program_module.program, view="gpm")

    if competence_id:
        comp = ProgramCompetence.objects.get(id=competence_id)
        program_module.competence = comp
    else:
        program_module.competence = None
    program_module.save()
    trigger.activate()
    return Response(status=200)


@api_view(("GET", ))
@permission_classes((AllowAny, ))
def heartbeat(request):
    return Response(status=200)


@api_view(('GET',))
@permission_classes((IsAuthenticatedOrReadOnly, ))
def get_program_disciplines(request, program_id):
    trigger = Changed.objects.filter(program__id=program_id, view="gpd").first()
    if not trigger:
        trigger = Changed.objects.create(program_id=program_id, view="gpd")
        trigger.activate()
        trigger.save()
    if not trigger.state():
        return Response(cache.get(f"gpd-{program_id}"))
    response = []
    disciplines = (Discipline.objects.filter(module__id__in=[mod.module.id for mod in ProgramModules.objects.filter(program__id=program_id, status="p", archived=False)], status="p", archived=False))
    for discipline in disciplines:
        terms = {}
        for term in TrainingTerms.objects.all().order_by("title"):
            semesters = [s.training_semester for s in Semester.objects.filter(discipline=discipline, term=term, program=program_id)]
            terms[term.title] = 0 if len(semesters) == 0 else min(semesters)

        response.append({
                    "id": discipline.id,
                    "title": discipline.title,
                    "module": discipline.module.title,
                    "labor": discipline.labor,
                    "period": discipline.period,
                    "terms": terms,
                    "priority": 9999 if not discipline.module.uni_priority else discipline.module.uni_priority
                    })
    cache.set(f"gpd-{program_id}", sorted(response, key=lambda k: (k["priority"], k["title"])), 2678400)
    trigger.deactivate()
    trigger.save()
    return Response(sorted(response, key=lambda k: (k["priority"], k["title"])))


@api_view(('POST',))
@permission_classes((DjangoModelPermissions, )) #
def change_discipline_semester(request):
    program = Program.objects.get(id=request.data["program_id"])
    discipline = Discipline.objects.get(id=request.data["discipline_id"])
    term_title = request.data["term_title"]
    new_semester = request.data["semester"]

    semester = Semester.objects.filter(program=program, discipline=discipline, term__title=term_title)
    if semester:
        semester.update(training_semester=new_semester, year=date.today().year)
    else:
        Semester.objects.create(program=program, discipline=discipline, term=TrainingTerms.objects.filter(title=term_title).first(), training_semester=new_semester, year=date.today().year)
    trigger = Changed.objects.filter(program=program, view="gpd").first()
    if not trigger:
        trigger = Changed.objects.create(program=program, view="gpd")
    trigger.activate()
    return Response(status=200)


@api_view(('GET',))
@permission_classes((IsAuthenticatedOrReadOnly, ))
def get_variants(request, program_id, discipline_id):
    trigger = Changed.objects.filter(program__id=program_id, view="gv").first()
    if not trigger:
        trigger = Changed.objects.create(program_id=program_id, view="gv")
        trigger.activate()
        trigger.save()
    if not trigger.state():
        return Response(cache.get(f"gv-{program_id}"))
    variants = Variant.objects.filter(program__id=program_id, discipline__id=discipline_id)
    response = [{
                    "id": variant.id,
                    "diagram": None if not variant.diagram else
                    {
                        "id": variant.diagram.id,
                        "title": variant.diagram.title,
                        "diagram": variant.diagram.diagram
                    },
                    "course": None if not variant.course else
                    {
                        "title": variant.course.title
                    },
                    "technology": None if not variant.technology else
                    {
                        "id": variant.technology.id,
                        "title": variant.technology.title,
                        "description": variant.technology.description,
                        "contact_work_category": variant.technology.contact_work_category,
                        "color": variant.technology.color
                    },
                    "semester": None if not variant.semester else
                    {
                        "term": variant.semester.term.title,
                        "training_semester": variant.semester.training_semester,
                    },
                    "parity": None if not variant.parity else variant.parity,
                    "link": variant.link
                     } for variant in variants]

    cache.set(f"gv-{program_id}", response, 2678400)
    trigger.deactivate()
    trigger.save()
    return Response(response)


@api_view(('POST',))
@permission_classes((DjangoModelPermissions, )) #
def change_variant(request):
    variant = get_object_or_404(Variant, pk=request.data["variant_id"])
    for key, value in request.data.items():
        if key != "variant_id" and key != "semester":
            value = request.data.get(key, None)
            if value:
                variant.__dict__[key] = value
            else:
                variant.__dict__[key] = None
        elif key == "semester":
            semester = Semester.objects.filter(discipline=variant.discipline, term__title=request.data[key], program=variant.program).first()
            if semester:
                variant.semester = semester

    variant.status = "p"
    variant.save()
    trigger = Changed.objects.filter(program=variant.program, view="gv").first()
    if not trigger:
        trigger = Changed.objects.create(program=variant.program, view="gv")
    trigger.activate()
    return Response(status=200)


@api_view(('POST',))
@permission_classes((DjangoModelPermissions, )) #
def create_variant(request):
    program = Program.objects.get(id=request.data["program_id"])
    discipline = Discipline.objects.get(id=request.data["discipline_id"])
    term_title = request.data.get("term_title", None)

    technology = request.data.get("technology_id", None)
    diagram = request.data.get("diagram_id", None)
    course = request.data.get("course_id", None)
    parity = request.data.get("parity_id", None)
    link = request.data.get("link", None)

    if term_title:
        semester = Semester.objects.filter(program=program, discipline=discipline, term__title=term_title).first()

        if Variant.objects.filter(discipline=discipline, program=program, semester=semester, technology=technology,
                               diagram=diagram, link=link, status="p").first():
            return Response(status=409)

        Variant.objects.create(discipline=discipline, program=program, semester=semester, technology=technology,
                               diagram=diagram, link=link, status="p")
    elif course:
        Variant.objects.create(discipline=discipline, program=program, technology=technology,
                               course=Course.objects.get(id=course), diagram=diagram, link=link, status="p")
    elif parity:
        Variant.objects.create(discipline=discipline, program=program, parity=parity, technology=technology,
                               diagram=diagram, link=link, status="p")
    trigger = Changed.objects.filter(program=program, view="gv").first()
    if not trigger:
        trigger = Changed.objects.create(program=program, view="gv")
    trigger.activate()
    return Response(status=200)


@api_view(('GET',))
@permission_classes((IsAuthenticatedOrReadOnly, ))
def get_program_variants(request, program_id):
    trigger = Changed.objects.filter(program__id=program_id, view="gv").first()
    if not trigger:
        trigger = Changed.objects.create(program_id=program_id, view="gv")
        trigger.activate()
        trigger.save()
    if not trigger.state():
        return Response(cache.get(f"gv-{program_id}"))
    variants = {}
    program = Program.objects.get(id=program_id)
    disciplines = program.get_all_disciplines()
    for discipline in disciplines:
        variants[discipline.id] = []
        for variant in Variant.objects.filter(program=program, discipline__id=discipline.id):
            variants[discipline.id].append(
                {
                    "id": variant.id,
                    "diagram": None if not variant.diagram else
                    {
                        "id": variant.diagram.id,
                        "title": variant.diagram.title,
                        "diagram": variant.diagram.diagram
                    },
                    "course": None if not variant.course else
                    {
                        "title": variant.course.title
                    },
                    "technology": None if not variant.technology else
                    {
                        "id": variant.technology.id,
                        "title": variant.technology.title,
                        "description": variant.technology.description,
                        "contact_work_category": variant.technology.contact_work_category,
                        "color": variant.technology.color
                    },
                    "semester": None if not variant.semester else
                    {
                        "term": variant.semester.term.title,
                        "training_semester": variant.semester.training_semester,
                    },
                    "parity": None if not variant.parity else variant.parity,
                    "link": variant.link
                }
            )
    cache.set(f"gv-{program_id}", variants, 2678400)
    trigger.deactivate()
    trigger.save()
    return Response(variants)


@api_view(('POST',))
@permission_classes((DjangoModelPermissions, )) #
def delete_variant(request):
    variant = get_object_or_404(Variant, pk=request.data["variant_id"])
    trigger = Changed.objects.filter(program=variant.program, view="gv").first()
    if not trigger:
        trigger = Changed.objects.create(program=variant.program, view="gv")
    trigger.activate()
    variant.delete()
    return Response(status=200)


@api_view(('POST',))
@permission_classes((AllowAny, )) #
def new_trajectory(request):
    program = Program.objects.get(id=request.data["program_id"])
    student_program = StudentProgram.objects.create(program=program)

    return Response(status=200, data={"link": student_program.link,
                                      "id": student_program.id}
                    )

@api_view(('POST',))
@permission_classes((AllowAny, )) #
def save_trajectory(request):
    student_program = StudentProgram.objects.get(id=request.data["id"])
    json = request.data.get("data", None)
    student_program.json = json
    student_program.save()

    return Response(status=200, data={"link": student_program.link,
                                      "id": student_program.id}
                    )

@api_view(('GET',))
@permission_classes((AllowAny, )) #
def get_trajectory_id(request, id):
    student_program = StudentProgram.objects.get(id=id)
    return Response({"id": student_program.id,
                     "link": student_program.link,
                     "user": None if not student_program.user else student_program.user.id,
                     "program": student_program.program.id,
                     "data": student_program.json,
                     })

@api_view(('GET',))
@permission_classes((IsAuthenticatedOrReadOnly, )) #
def get_trajectory_link(request, link):
    student_program = StudentProgram.objects.filter(link=link).first()
    return Response({"id": student_program.id,
                     "link": student_program.link,
                     "user": None if not student_program.user else student_program.user.id,
                     "program": student_program.program.id,
                     "data": student_program.json,
                     })


@api_view(('GET',))
@permission_classes((IsAuthenticatedOrReadOnly, )) #
def get_program_trajectory(request, program_id):
    response = []
    student_programs = StudentProgram.objects.filter(program__id=program_id)

    for student_program in student_programs:
        response.append(
            {"id": student_program.id,
             "link": student_program.link,
             "user": None if not student_program.user else student_program.user.id,
             "program": student_program.program.id,
             "data": student_program.json,
             }
        )

    return Response(response)

@api_view(('POST',))
@permission_classes((AllowAny, )) #
def delete_trajectory(request):
    StudentProgram.objects.remove(id=request.data["id"])
    return Response(status=200)
