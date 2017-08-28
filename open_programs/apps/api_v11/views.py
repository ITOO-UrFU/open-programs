from datetime import date

import jwt
from cms.api_views import *
from competences.models import Competence
from competences.serializers import CompetenceSerializer
from courses.models import Course
from courses.serializers import CourseSerializer
from disciplines.models import Discipline, Semester, TrainingTerms, Diagram, Technology, Variant
from disciplines.serializers import *
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from modules.models import Module, Type
from modules.serializers import ModuleSerializer, TypeSerializer
from persons.models import Person
from persons.serializers import UserSerializer, PersonSerializer
from programs.models import Program, TrainingTarget, ProgramCompetence, ProgramModules, \
    TargetModules, ChoiceGroup, ChoiceGroupType, Changed, StudentProgram
from programs.serializers import ProgramSerializer, TrainingTargetSerializer, \
    ProgramCompetenceSerializer, ChoiceGroupTypeSerializer, \
    ChoiceGroupSerializer, ProgramModulesSerializer, TargetModulesSerializer, StudentProgramSerializer, \
    StudentProgramSerializer_nouser
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, BasePermission, \
    DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from results.models import Result
from results.serializers import ResultSerializer


def get_user_by_jwt(request):
    jwt_token = request.META.get('HTTP_AUTHORIZATION', None)
    if jwt_token:
        try:
            token_data = jwt.decode(jwt_token, settings.SECRET_KEY)
        except jwt.exceptions.ExpiredSignatureError:
            return AnonymousUser
        return User.objects.get(pk=token_data['user_id'])
    else:
        return AnonymousUser


class IsManager(BasePermission):
    def has_permission(self, request, view):
        user = get_user_by_jwt(request)
        if user and not user.is_anonymous:
            return user.groups.filter(name='manager').exists()
        else:
            return False


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        user = get_user_by_jwt(request)
        if user and not user.is_anonymous:
            return True
        else:
            return False


IsAuthorized = IsStudent


class ProgramList(viewsets.ModelViewSet):  # CacheResponseMixin,
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


class ModuleList(CacheResponseMixin, viewsets.ModelViewSet):
    queryset = Module.objects.filter(status="p", archived=False)
    serializer_class = ModuleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)


class TypeList(CacheResponseMixin, viewsets.ModelViewSet):
    queryset = Type.objects.filter(status="p", archived=False)
    serializer_class = TypeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)


class DisciplineList(CacheResponseMixin, viewsets.ModelViewSet):
    queryset = Discipline.objects.filter(archived=False)
    serializer_class = DisciplineSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)


class ResultList(CacheResponseMixin, viewsets.ModelViewSet):
    queryset = Result.objects.filter(status="p", archived=False)
    serializer_class = ResultSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)


class CompetenceList(CacheResponseMixin, viewsets.ModelViewSet):
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
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)


class CourseList(viewsets.ModelViewSet):  ##CacheResponseMixin,
    queryset = Course.objects.filter(status="p", archived=False)
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)


class UserList(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)


class TrainingTargetList(CacheResponseMixin, viewsets.ModelViewSet):
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


class TargetModulesList(CacheResponseMixin, viewsets.ModelViewSet):
    queryset = TargetModules.objects.filter(status="p", archived=False)
    serializer_class = TargetModulesSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)


class ChoiceGroupList(CacheResponseMixin, viewsets.ModelViewSet):
    queryset = ChoiceGroup.objects.filter(status="p", archived=False)
    serializer_class = ChoiceGroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)


class ChoiceGroupTypeList(CacheResponseMixin, viewsets.ModelViewSet):
    queryset = ChoiceGroupType.objects.filter(status="p", archived=False)
    serializer_class = ChoiceGroupTypeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)


class DiagramList(CacheResponseMixin, viewsets.ModelViewSet):
    queryset = Diagram.objects.filter(status="p", archived=False)
    serializer_class = DiagramSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)


class TechnologyList(CacheResponseMixin, viewsets.ModelViewSet):
    serializer_class = TechnologySerializer
    queryset = Technology.objects.filter(status="p", archived=False)
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)


class TrainingTermsList(CacheResponseMixin, viewsets.ModelViewSet):
    serializer_class = TrainingTermsSerializer
    queryset = TrainingTerms.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)


class SemesterList(CacheResponseMixin, viewsets.ModelViewSet):
    serializer_class = SemesterSerializer
    queryset = Semester.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)


class VariantList(CacheResponseMixin, viewsets.ModelViewSet):
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
@permission_classes((IsAuthenticatedOrReadOnly,))
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


def _check_trigger(cache_key=None):
    trigger = Changed.objects.filter(view=cache_key).first()
    if not trigger:
        trigger = Changed.objects.create(view=cache_key)
        trigger.activate()
        trigger.save()
    if not trigger.state():
        return Response(cache.get(cache_key))


def _activate_trigger(cache_key=None):
    trigger = Changed.objects.filter(view=cache_key).first()
    if not trigger:
        trigger = Changed.objects.create(view=cache_key)
        trigger.activate()
        trigger.save()


def _cache(cache_key=None, response=None):
    trigger = Changed.objects.filter(view=cache_key).first()
    if trigger:
        cache.set(cache_key, response, 2678400)
        trigger.deactivate()
        trigger.save()


@api_view(('GET',))
@permission_classes((IsAuthenticatedOrReadOnly,))
def get_targets_by_program(request, program_id):
    # response = _check_trigger(f"get_targets_by_program:{program_id}")
    # if response:
    #     return response
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

    # _cache(f"get_targets_by_program:{program_id}", response)

    return Response(response)


@api_view(('GET',))
@permission_classes((IsAuthenticatedOrReadOnly,))
def get_competences_by_program(request, program_id):
    response = [{"id": c.id,
                 "title": c.title,
                 "number": c.number,
                 } for c in ProgramCompetence.objects.filter(program__id=program_id)]
    return Response(sorted(response, key=lambda k: k['number']))


@api_view(('GET',))
@permission_classes((IsAuthenticatedOrReadOnly,))
def get_program_modules(request, program_id):
    # response = _check_trigger(f"get_program_modules:{program_id}")
    # if response:
    #     return response
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
            "uni_coordinator": None if not mod.module.uni_coordinator else mod.module.uni_coordinator,
            "disciplines": mod.get_all_discipline_custom()
        })
    response = sorted(response, key=lambda k: (k["semester"], k["priority"], k["title"]))
    # _cache(f"get_program_modules:{program_id}", response)
    return Response(response)


class ChangeTargetModule(APIView):
    permission_classes = (IsManager,)

    def post(self, request):
        module_id = request.data["module_id"]
        target_id = request.data["target_id"]
        status = request.data["status"]

        program_module = ProgramModules.objects.get(id=module_id)
        target = TrainingTarget.objects.get(id=target_id)
        status = int(status)
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
        # _activate_trigger(f"get_program_modules:{program_module.program.id}")
        return Response(status=200)


class ChangeChoiceGroup(APIView):
    permission_classes = (IsManager,)

    def post(self, request):
        module_id = request.data["module_id"]
        choice_group_id = request.data["choice_group_id"]
        program_module = ProgramModules.objects.get(id=module_id)

        if choice_group_id:
            chg = ChoiceGroup.objects.get(id=choice_group_id)
            program_module.choice_group = chg
        else:
            program_module.choice_group = None

        program_module.save()
        # _activate_trigger(f"get_program_modules:{program_module.program.id}")
        return Response(status=200)


class ChangeCompetence(APIView):
    permission_classes = (IsManager,)

    def post(self, request):
        module_id = request.data["module_id"]
        competence_id = request.data["competence_id"]
        program_module = ProgramModules.objects.get(id=module_id)

        if competence_id:
            comp = ProgramCompetence.objects.get(id=competence_id)
            program_module.competence = comp
        else:
            program_module.competence = None
        program_module.save()
        # _activate_trigger(f"get_program_modules:{program_module.program.id}")
        return Response(status=200)


@api_view(("GET",))
@permission_classes((AllowAny,))
def heartbeat(request):
    return Response(status=200)


@api_view(('GET',))
@permission_classes((IsAuthenticatedOrReadOnly,))
def get_program_disciplines(request, program_id):
    # response = _check_trigger(f"get_program_disciplines:{program_id}")
    # if response:
    #     return response
    response = []
    disciplines = (Discipline.objects.filter(module__id__in=[mod.module.id for mod in
                                                             ProgramModules.objects.filter(program__id=program_id,
                                                                                           status="p",
                                                                                           archived=False).order_by(
                                                                 "index")],
                                             status="p", archived=False))
    for discipline in disciplines:
        terms = {}
        for term in TrainingTerms.objects.all().order_by("title"):
            semesters = [s.training_semester for s in
                         Semester.objects.filter(discipline=discipline, term=term, program=program_id)]
            terms[term.title] = 0 if len(semesters) == 0 else min(semesters)

        response.append({
            "id": discipline.id,
            "title": discipline.title,
            "module": discipline.module.title,
            "module_uni_number": None if not discipline.module.uni_number else discipline.module.uni_number,
            "labor": discipline.labor,
            "period": discipline.period,
            "terms": terms,
            "priority": 9999 if not discipline.module.uni_priority else discipline.module.uni_priority
        })

    response = sorted(response, key=lambda k: (k["priority"], k["title"]))
    # _cache(f"get_program_disciplines:{program_id}", response)
    return Response(response)


@api_view(('GET',))
@permission_classes((IsAuthenticatedOrReadOnly,))
def get_program_discipline(request, program_id, discipline_id):
    # response = _check_trigger(f"get_program_discipline:{program_id}")
    # if response:
    #     return response

    discipline = Discipline.objects.get(id=discipline_id)
    terms = {}
    for term in TrainingTerms.objects.all().order_by("title"):
        semesters = [s.training_semester for s in
                     Semester.objects.filter(discipline=discipline, term=term, program=program_id)]
        terms[term.title] = 0 if len(semesters) == 0 else min(semesters)

    response = {
        "id": discipline.id,
        "title": discipline.title,
        "module": discipline.module.title,
        "module_uni_number": None if not discipline.module.uni_number else discipline.module.uni_number,
        "labor": discipline.labor,
        "period": discipline.period,
        "terms": terms,
        "priority": 9999 if not discipline.module.uni_priority else discipline.module.uni_priority
    }
    # _cache(f"get_program_discipline:{program_id}", response)
    return Response(response)


class ChangeDisciplineSemester(APIView):
    permission_classes = (IsManager,)

    def post(self, request):
        program = Program.objects.get(id=request.data["program_id"])
        discipline = Discipline.objects.get(id=request.data["discipline_id"])
        term_title = request.data["term_title"]
        new_semester = request.data["semester"]

        semester = Semester.objects.filter(program=program, discipline=discipline, term__title=term_title)
        if semester:
            semester.update(training_semester=new_semester, year=date.today().year)
        else:
            Semester.objects.create(program=program, discipline=discipline,
                                    term=TrainingTerms.objects.filter(title=term_title).first(),
                                    training_semester=new_semester, year=date.today().year)
        # _activate_trigger(f"get_program_disciplines:{program.id}")
        # _activate_trigger(f"get_program_discipline:{program.id}")
        return Response(status=200)


@api_view(('GET',))
@permission_classes((IsAuthenticatedOrReadOnly,))
def get_variants(request, program_id, discipline_id):
    # response = _check_trigger(f"get_variants:{program_id}:{discipline_id}")
    # if response:
    #     return response
    variants = Variant.objects.filter(program__id=program_id, discipline__id=discipline_id).order_by("semester__term")
    response = []
    for variant in variants:
        if variant.diagram:

            if variant.semester:
                mobility = 0
            elif variant.parity:
                mobility = 50
            elif variant.course:
                mobility = 100
            else:
                mobility = None

            if "очно-заочн" in variant.diagram.title.lower():
                presence = "oz"
            elif 'заоч' in variant.diagram.title.lower():
                presence = "z"
            # elif 'лайн' in variant.technology.title.lower():
            #     presence = 'online'
            else:
                presence = "o"

            # if "традиционная" in variant.technology.title.lower():
            technology_type = "t"
            # else:
            #     technology_type = "d"

        response.append(
            {
                "id": variant.id,

                "diagram": None if not variant.diagram else
                {
                    "id": variant.diagram.id,
                    "title": variant.diagram.title,
                    # "diagram": variant.diagram.diagram
                },
                "course": None if not variant.course else
                {
                    "title": variant.course.title
                },
                "technology": None if not variant.diagram else
                {
                    "sync": None if not variant.diagram else int(variant.diagram.sync),
                    "campus": None if not variant.diagram else int(variant.diagram.campus),
                    "mobility": mobility,
                    "presence": presence,
                    "technology_type": technology_type,

                },
                "sync": None if not variant.diagram else int(variant.diagram.sync),
                "campus": None if not variant.diagram else int(variant.diagram.campus),
                "mobility": mobility,
                "semester": None if not variant.semester else
                {
                    "term": variant.semester.term.title,
                    "training_semester": variant.semester.training_semester,
                },
                "parity": None if not variant.parity else variant.parity,
                "link": variant.link
            }
        )

    # response = [{
    #                 "id": variant.id,
    #                 "diagram": None if not variant.diagram else
    #                 {
    #                     "id": variant.diagram.id,
    #                     "title": variant.diagram.title,
    #                     "diagram": variant.diagram.diagram
    #                 },
    #                 "course": None if not variant.course else
    #                 {
    #                     "title": variant.course.title
    #                 },
    #                 "technology": None if not variant.technology else
    #                 {
    #                     "id": variant.technology.id,
    #                     "title": variant.technology.title,
    #                     "description": variant.technology.description,
    #                     "contact_work_category": variant.technology.contact_work_category,
    #                     "color": variant.technology.color
    #                 },
    #                 "semester": None if not variant.semester else
    #                 {
    #                     "term": variant.semester.term.title,
    #                     "training_semester": variant.semester.training_semester,
    #                 },
    #                 "parity": None if not variant.parity else variant.parity,
    #                 "link": variant.link
    #             } for variant in variants]

    # _cache(f"get_variants:{program_id}:{discipline_id}", response)
    return Response(response)


class ChangeVariant(APIView):
    permission_classes = (IsManager,)

    def post(self, request):
        variant = get_object_or_404(Variant, pk=request.data["variant_id"])
        for key, value in request.data.items():
            if key != "variant_id" and key != "semester":
                value = request.data.get(key, None)
                if value:
                    variant.__dict__[key] = value
                else:
                    variant.__dict__[key] = None
            elif key == "semester":
                semester = Semester.objects.filter(discipline=variant.discipline, term__title=request.data[key],
                                                   program=variant.program).first()
                if semester:
                    variant.semester = semester

        variant.status = "p"
        variant.save()
        # _activate_trigger(f"get_variants:{variant.program.id}:{variant.discipline.id}")
        return Response(status=200)


class CreateVariant(APIView):
    permission_classes = (IsManager,)

    def post(self, request):
        program = Program.objects.get(id=request.data["program_id"])
        discipline = Discipline.objects.get(id=request.data["discipline_id"])
        term_title = request.data.get("term_title", None)

        diagram = request.data.get("diagram_id", None)
        course = request.data.get("course_id", None)
        parity = request.data.get("parity_id", None)
        link = request.data.get("link", None)

        if term_title:
            semester = Semester.objects.filter(program=program, discipline=discipline, term__title=term_title).first()

            if Variant.objects.filter(discipline=discipline, program=program, semester=semester,
                                      diagram=diagram, link=link, status="p").first():
                return Response(status=409)

            variant = Variant.objects.create(discipline=discipline, program=program, semester=semester,
                                             diagram=diagram, link=link, status="p")
        elif course:
            variant = Variant.objects.create(discipline=discipline, program=program,
                                             course=Course.objects.get(id=course), diagram=diagram, link=link,
                                             status="p")
        elif parity:
            variant = Variant.objects.create(discipline=discipline, program=program, parity=parity,
                                             diagram=diagram, link=link, status="p")
        # _activate_trigger(f"get_variants:{request.data['program_id']}:{request.data['discipline_id']}")
        # _activate_trigger(f"get_program_variants_constructor:{request.data['program_id']}")
        # _activate_trigger(f"get_program_variants:{request.data['program_id']}")
        return Response(status=200)


@api_view(('GET',))
@permission_classes((IsAuthenticatedOrReadOnly,))
def get_program_variants(request, program_id):
    # response = _check_trigger(f"get_program_variants:{program_id}")
    # if response:
    #     return response
    variants = {}
    program = Program.objects.get(id=program_id)
    disciplines = program.get_all_disciplines()
    for discipline in disciplines:
        variants[discipline.id] = []
        for variant in Variant.objects.filter(program=program, discipline__id=discipline.id).order_by("semester__term"):

            if variant.semester:
                mobility = 0
            elif variant.parity:
                mobility = 50
            elif variant.course:
                mobility = 100

            if variant.diagram:
                if 'заоч' in variant.diagram.title.lower():
                    presence = "z"
                # elif 'лайн' in variant.diagram.title.lower():
                #     presence = 'online'
                else:
                    presence = "o"

                # if "традиционная" in variant.technology.title.lower():
                technology_type = "t"
                # else:
                #     technology_type = "d"

            variants[discipline.id].append(
                {
                    "id": variant.id,
                    "diagram": None if not variant.diagram else
                    {
                        "id": variant.diagram.id,
                        "title": variant.diagram.title,
                        # "diagram": variant.diagram.diagram
                    },
                    "course": None if not variant.course else
                    {
                        "title": variant.course.title
                    },
                    "technology": None if not variant.diagram else
                    {
                        "sync": None if not variant.diagram else int(variant.diagram.sync),
                        "campus": None if not variant.diagram else int(variant.diagram.campus),
                        "mobility": mobility,
                        "presence": presence,
                        "technology_type": technology_type,

                    },
                    "sync": None if not variant.diagram else int(variant.diagram.sync),
                    "campus": None if not variant.diagram else int(variant.diagram.campus),
                    "mobility": mobility,
                    "semester": None if not variant.semester else
                    {
                        "term": variant.semester.term.title,
                        "training_semester": variant.semester.training_semester,
                    },
                    "parity": None if not variant.parity else variant.parity,
                    "link": variant.link
                }
            )
    # _cache(f"get_program_variants:{program_id}", variants)
    return Response(variants)


@api_view(('GET',))
@permission_classes((IsAuthenticatedOrReadOnly,))
def get_program_variants_constructor(request, program_id):
    # response = _check_trigger(f"get_program_variants_constructor:{program_id}")
    # if response:
    #     return response
    variants = {}
    program = Program.objects.get(id=program_id)
    disciplines = program.get_all_disciplines()
    for discipline in disciplines:
        variants[discipline.id] = []
        for variant in Variant.objects.filter(program=program, discipline__id=discipline.id).order_by("semester__term"):
            if variant.semester:
                mobility = 0
            elif variant.parity:
                mobility = 50
            elif variant.course:
                mobility = 100
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
                    "technology": None if not variant.diagram else
                    {
                        "sync": None if not variant.diagram.sync else int(variant.diagram.sync),
                        "campus": None if not variant.diagram.campus else int(variant.diagram.campus),
                        "mobility": mobility,
                    },
                    "sync": None if not variant.diagram else int(variant.diagram.sync),
                    "campus": None if not variant.diagram else int(variant.diagram.campus),
                    "mobility": mobility,
                    "semester": None if not variant.semester else
                    {
                        "term": variant.semester.term.title,
                        "training_semester": variant.semester.training_semester,
                    },
                    "parity": None if not variant.parity else variant.parity,
                    "link": variant.link
                }
            )
    # _cache(f"get_program_variants_constructor:{program_id}", variants)
    return Response(variants)


class DeleteVariant(APIView):
    permission_classes = (IsManager,)

    def post(self, request):
        variant = get_object_or_404(Variant, pk=request.data["variant_id"])
        # _activate_trigger(f"get_program_variants_constructor:{variant.program.id}")
        # _activate_trigger(f"get_program_variants:{variant.program.id}")
        # _activate_trigger(f"get_variants:{variant.program.id}:{variant.discipline.id}")
        variant.delete()
        return Response(status=200)


@api_view(('POST',))
@permission_classes((AllowAny,))  #
def new_trajectory(request):
    program = Program.objects.get(id=request.data["program_id"])
    student_program = StudentProgram.objects.create(program=program)

    return Response(status=200, data={"link": student_program.link,
                                      "id": student_program.id}
                    )


@api_view(('POST',))
@permission_classes((AllowAny,))  #
def save_trajectory(request):
    student_program = StudentProgram.objects.get(id=request.data["id"])
    json = request.data.get("data", None)
    student_program.json = json
    student_program.user = None if get_user_by_jwt(request).is_anonymous else get_user_by_jwt(request)
    student_program.save()

    print(student_program.user, "USER")

    return Response(status=200, data={"link": student_program.link,
                                      "id": student_program.id}
                    )


@api_view(('GET',))
@permission_classes((AllowAny,))  #
def get_trajectory_id(request, id):
    student_program = StudentProgram.objects.get(id=id)
    return Response({"id": student_program.id,
                     "link": student_program.link,
                     "user": None if not student_program.user else student_program.user.id,
                     "program": student_program.program.id,
                     "data": student_program.json,
                     "program_name": student_program.program.title,
                     })


@api_view(('GET',))
@permission_classes((IsAuthenticatedOrReadOnly,))  #
def get_trajectory_link(request, link):
    student_program = StudentProgram.objects.filter(link=link).first()
    return Response({"id": student_program.id,
                     "link": student_program.link,
                     "user": None if not student_program.user else student_program.user.id,
                     "program": student_program.program.id,
                     "data": student_program.json,
                     "program_name": student_program.program.title,
                     })


class GetTrajectories(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        user = get_user_by_jwt(request)
        if user:
            student_programs = StudentProgram.objects.filter(user=user)
            student_programs = StudentProgramSerializer_nouser(student_programs, many=True)
            return Response(student_programs.data, status=200)
        else:
            return Response(status=204)


@api_view(('GET',))
@permission_classes((IsAuthenticatedOrReadOnly,))
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
             "program_name": student_program.program.title,
             }
        )

    return Response(response)


@api_view(('POST',))
@permission_classes((IsStudent,))
def delete_trajectory(request):
    user = get_user_by_jwt(request)
    id = request.data.get("id", "")
    if id != "":
        sp = StudentProgram.objects.get(pk=id)
        if sp.user == user:
            StudentProgram.objects.get(pk=id).delete()
        else:
            return Response(status=403)
    else:
        return Response(status=403)
    return Response(status=200)


@api_view(('POST',))
@permission_classes((IsStudent,))
def copy_trajectory(request):
    user = get_user_by_jwt(request)
    id = request.data.get("id", "")
    if id != "":
        sp = StudentProgram.objects.get(pk=id)
        if sp.user == user:
            new_sp = StudentProgram.objects.create(
                program=sp.program,
                user=sp.user,
                json=sp.json,
            )
            return Response({"id": new_sp.id,
                             "link": new_sp.link,
                             "user": new_sp.user.id,
                             "program": new_sp.program.id,
                             "data": new_sp.json,
                             "program_name": new_sp.program.title,
                             })
        else:
            return Response(status=403)
    else:
        return Response(status=403)


@api_view(('POST',))
@permission_classes((IsManager,))
def remove_discipline(request):
    id = request.data.get("id", "")
    if id != "":
        d = Discipline.objects.get(pk=id)
        d.archived = True
        d.save()
    else:
        return Response(status=403)
    return Response(status=200)


@api_view(('POST',))
@permission_classes((IsManager,))
def add_default_variants(request):
    discipline_id = request.data.get("discipline_id", "")
    program_id = request.data.get("program_id", "")
    if id != "":
        discipline = Discipline.objects.get(pk=discipline_id)
        program = Program.objects.get(pk=program_id)

        _terms = []
        for semester in Semester.objects.filter(discipline=discipline, program=program):
            if semester.term in _terms:
                semester.delete()
            else:
                _terms.append(semester.term)

        for semester in Semester.objects.filter(discipline=discipline, program=program):
            print(semester.term.title)
            if "4 года" in semester.term.title:
                variants = Variant.objects.filter(discipline=discipline, program=program, semester=semester)
                if "Традиционная очная форма" not in [variant.diagram.title for variant in variants]:
                    print("added", semester.term.title, "Традиционная очная форма")
                    print("\n".join([variant.diagram.title for variant in variants]))
                    print()
                    Variant.objects.create(
                        discipline=discipline,
                        program=program,
                        diagram=Diagram.objects.filter(title="Традиционная очная форма", status="p",
                                                       archived=False).first(),
                        semester=semester
                    )
                if "Очная форма с применением ЭО и ДОТ без выезда в кампус" not in [variant.diagram.title for variant in
                                                                                    variants]:
                    Variant.objects.create(
                        discipline=discipline,
                        program=program,
                        diagram=Diagram.objects.filter(title="Очная форма с применением ЭО и ДОТ без выезда в кампус",
                                                       status="p", archived=False).first(),
                        semester=semester
                    )
            else:
                variants = Variant.objects.filter(discipline=discipline, program=program, semester=semester)
                if "Традиционная заочная форма" not in [variant.diagram.title for variant in variants]:
                    Variant.objects.create(
                        discipline=discipline,
                        program=program,
                        diagram=Diagram.objects.filter(title="Традиционная заочная форма", status="p",
                                                       archived=False).first(),
                        semester=semester
                    )
                if "Заочная форма с применением ЭО и ДОТ без выезда в кампус" not in [variant.diagram.title for variant
                                                                                      in variants]:
                    Variant.objects.create(
                        discipline=discipline,
                        program=program,
                        diagram=Diagram.objects.filter(title="Заочная форма с применением ЭО и ДОТ без выезда в кампус",
                                                       status="p", archived=False).first(),
                        semester=semester
                    )

    else:
        return Response(status=403)
    return Response({"message": "ok"})


change_target_module = ChangeTargetModule.as_view()
change_choice_group = ChangeChoiceGroup.as_view()
change_competence = ChangeCompetence.as_view()
change_discipline_semester = ChangeDisciplineSemester.as_view()
change_variant = ChangeVariant.as_view()
create_variant = CreateVariant.as_view()
delete_variant = DeleteVariant.as_view()

get_trajectories = GetTrajectories.as_view()
