import uuid

from django.db import models
from base.models import ObjectBaseClass
from django.utils.translation import ugettext_lazy as _

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
    
    
class ProgramCompetence(ObjectBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('Наименование компетенции'), blank=False, max_length=2048, default=_(''))
    program = models.ForeignKey("Program", blank=True, null=True)
    number = models.IntegerField(_("Номер компетенции"))

    class Meta:
        verbose_name = 'компетенция программы'
        verbose_name_plural = 'компетенции программы'

    def __str__(self):
        return self.title


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

        training_targets = TrainingTarget.objects.filter(program=self.program, ).order_by('number')
        for training_target in training_targets:
            target_modules = TargetModules.objects.filter(target=training_target, program_module=self).values_list("choice_group", flat=True)
            print(target_modules)
        targets_positions = []
        # for tr_target in TrainingTarget.objects.filter(program=self.program, ).order_by('number'):
        #     tms = TargetModules.objects.filter(target=tr_target, status="p", archived=False).values_list("choice_group", flat=True)
        #     print(tms)
        #
        #     for target_module in tms:
        #         print(target_module)
        #         if target_module:
        #             if target_module is False:
        #                 targets_positions.append(1)
        #             elif target_module is True:
        #                 targets_positions.append(2)
        #         else:
        #             targets_positions.append(0)
        #
        # # except:
        # #     pass
        return targets_positions


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
        return [program_module.id for program_module in ProgramModules.objects.filter(program=self.program, choice_group=self, status="p", archived=False)]


class ChoiceGroupType(ObjectBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('Наименование типы группы выбора'), blank=False, max_length=2048, default=_(''))

    class Meta:
        verbose_name = 'тип группы выбора'
        verbose_name_plural = 'типы группы выбора'

    def __str__(self):
        return self.title
