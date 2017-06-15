import uuid
from os import urandom
import hashlib
from jsonfield import JSONField

from django.db import models
from base.models import ObjectBaseClass
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from persons.models import Person
from competences.models import Competence
from modules.models import Module
from disciplines.models import Discipline



class LearningPlan(ObjectBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uni_displayableTitle = models.CharField(_("Версия"), max_length=32, blank=True, null=True)
    uni_number = models.CharField(_("Номер УП"), max_length=32, blank=True, null=True)
    uni_active = models.CharField(_("Текущая версия"), max_length=32, blank=True, null=True)
    uni_title = models.CharField(_("Название"), max_length=32, blank=True, null=True)
    uni_stage = models.BooleanField(_("План утверждён"), default=True)
    uni_loadTimeType = models.CharField(_("Единица измерения нагрузки"), max_length=32, blank=True, null=True)
    uni_html = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.uni_number

    class Meta:
        verbose_name = 'учебный план'
        verbose_name_plural = 'учебные планы'


class Program(ObjectBaseClass):

    LEVELS = (
        ("b", _("бакалавриат")),
        ("m", _("магистратура")),
        ("s", _("специалитет")),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    level = models.CharField(_("Уровень программы"), max_length=1, choices=LEVELS, default="b")
    title = models.CharField(_('Наименование образовательной программы'), blank=False, max_length=256, default=_(''))
    training_direction = models.CharField(_("Направление подготовки"), blank=False, max_length=256, default=_(''))
    competences = models.ManyToManyField(Competence, blank=True)
    chief = models.ForeignKey(Person, verbose_name=_('Руководитель образовательной программы'), blank=True, null=True)
    learning_plans = models.ManyToManyField("LearningPlan", blank=True)

    class Meta:
        verbose_name = 'программа'
        verbose_name_plural = 'программы'

    def __str__(self):
        return self.title

    def get_choice_groups(self):
        return [choice_group.id for choice_group in ChoiceGroup.objects.filter(program__id=self.id)]

    def get_modules(self):
        return

    def get_all_disciplines(self):
        pms = ProgramModules.objects.filter(program=self, status="p", archived=False).values_list("module__id", flat=True)
        return Discipline.objects.filter(module__id__in=pms, status="p", archived=False)

    def get_competences_diagram(self):
        response = {}
        for target in TrainingTarget.objects.filter(program=self, status="p", archived=False).order_by("number"):
            response[target.title] = []
            for competence in ProgramCompetence.objects.filter(program=self):
                labors = [pm.module.get_labor() for pm in
                          ProgramModules.objects.filter(program=self, competence=competence, status="p", archived=False,
                                                        module__id__in=target.get_mandatory_modules_id())]
                response[target.title].append(
                    ([competence.title, competence.color, sum([0 if not labor else labor for labor in labors])]))

        return response


class TrainingTarget(ObjectBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('Наименование образовательной цели'), blank=False, max_length=256, default=_(''))
    program = models.ForeignKey("Program", blank=True, null=True)
    number = models.IntegerField(_("Порядковый номер цели"))

    class Meta:
        verbose_name = 'образовательная цель'
        verbose_name_plural = 'образовательные цели'

    def __str__(self):
        return self.title

    def get_modules_id(self):
        return TargetModules.objects.filter(target=self, archived=False, status="p").values_list(
            'program_module__module__id', flat=True)

    def get_mandatory_modules_id(self):
        return TargetModules.objects.filter(target=self, archived=False, status="p", choice_group=False).values_list(
            'program_module__module__id', flat=True)

    def get_choice_modules_id(self):
        return TargetModules.objects.filter(target=self, archived=False, status="p", choice_group=True).values_list(
            'program_module__module__id', flat=True)

    
class ProgramCompetence(ObjectBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('Наименование компетенции'), blank=False, max_length=2048, default=_(''))
    program = models.ForeignKey("Program", blank=True, null=True)
    number = models.IntegerField(_("Номер компетенции"))
    color = models.CharField(_("Цвет"), max_length=32, blank=True, null=True, default="green")

    class Meta:
        verbose_name = 'компетенция программы'
        verbose_name_plural = 'компетенции программы'

    def __str__(self):
        return self.title

    def get_labor(self):
        response = [pm.module.get_labor() for pm in
                    ProgramModules.objects.filter(program=self.program, competence=self, status="p", archived=False)]
        return sum([0 if not labor else labor for labor in response])


class ProgramModules(ObjectBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    program = models.ForeignKey("Program")
    module = models.ForeignKey("modules.Module")
    choice_group = models.ForeignKey("ChoiceGroup", blank=True, null=True)
    competence = models.ForeignKey(ProgramCompetence, blank=True, null=True)
    semester = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'модуль программы'
        verbose_name_plural = 'модули программы'

    def get_competence_display(self):
        return str(self.competence)

    def get_weight(self):
        try:
            weight = max([int(ds["period"]) for ds in
                          Discipline.objects.filter(pk__in=self.module.get_all_discipline_ids()).values(
                              "period")]) + self.semester
        except:
            weight = self.semester

        try:
            return int(weight) * 100
        except:
            return 100

    def get_target_positions(self):
        targets_positions = []
        try:
            tr_targets = TrainingTarget.objects.filter(program=self.program).order_by('number')
            for tt in tr_targets:
                tms = TargetModules.objects.filter(program_module=self, target=tt, status="p",
                                                   archived=False)
                if not tms:
                    status = 0
                for target_module in tms:
                    if target_module.choice_group is False:
                        status = 1
                    elif target_module.choice_group is True:
                        status = 2
                targets_positions.append(status)

        except:
            pass
        return targets_positions


class Changed(models.Model):
    _changed = models.BooleanField(default=True)
    program = models.ForeignKey("Program", null=True)
    view = models.CharField(max_length=16, blank=True, null=True)

    def state(self):
        return self._changed

    def activate(self):
        self._changed = True
        self.save()

    def deactivate(self):
        self._changed = False
        self.save()


class TargetModules(ObjectBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    target = models.ForeignKey("TrainingTarget")
    program_module = models.ForeignKey("ProgramModules")
    choice_group = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'модуль цели'
        verbose_name_plural = 'модули цели'


class ChoiceGroup(ObjectBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    program = models.ForeignKey("Program")
    title = models.CharField(_('Наименование группы выбора'), blank=False, max_length=2048, default=_(''))
    labor = models.IntegerField(_("Трудоёмкость группы"), default=3)
    choice_group_type = models.ForeignKey("ChoiceGroupType")
    number = models.IntegerField(_("Номер группы выбора"))

    class Meta:
        verbose_name = 'группа выбора'
        verbose_name_plural = 'группы выбора'

    def __str__(self):
        return self.title

    def get_choice_group_type_display(self):
        return self.choice_group_type.title

    def get_program_modules(self):
        return [program_module.id for program_module in
                ProgramModules.objects.filter(program=self.program, choice_group=self, status="p", archived=False)]


class ChoiceGroupType(ObjectBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('Наименование типы группы выбора'), blank=False, max_length=2048, default=_(''))

    class Meta:
        verbose_name = 'тип группы выбора'
        verbose_name_plural = 'типы группы выбора'

    def __str__(self):
        return self.title


def student_program_key():
    return str(hashlib.md5(urandom(128)).hexdigest()[:6])


class StudentProgram(ObjectBaseClass):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    link = models.CharField(unique=True, max_length=6, default=student_program_key)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True)
    program = models.ForeignKey("Program")
    json = JSONField(verbose_name=_("JSON"), null=True, blank=True)

    class Meta:
        verbose_name = 'сохранение'
        verbose_name_plural = 'сохранения'

    def __str__(self):
        return self.title


