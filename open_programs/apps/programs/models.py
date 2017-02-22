import uuid

from django.db import models
from base.models import ObjectBaseClass
from django.utils.translation import ugettext_lazy as _

from persons.models import Person
from competences.models import Competence
from modules.models import Module


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

    class Meta:
        verbose_name = 'программа'
        verbose_name_plural = 'программы'

    def __str__(self):
        return self.title

    def get_choice_groups(self):
        return [choice_group.id for choice_group in ChoiceGroup.objects.filter(program__id=self.id)]


class TrainingTarget(ObjectBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('Наименование образовательной цели'), blank=False, max_length=256, default=_(''))
    program = models.ManyToManyField("Program")
    number = models.IntegerField(_("Порядковый номер цели"))

    class Meta:
        verbose_name = 'образовательная цель'
        verbose_name_plural = 'образовательные цели'

    def __str__(self):
        return self.title
    
    
class ProgramCompetence(ObjectBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('Наименование компетенции'), blank=False, max_length=2048, default=_(''))
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
    choice_group = models.ForeignKey("ChoiceGroup")
    competence = models.ManyToManyField(ProgramCompetence, blank=True)
    period_start = models.DateField(_("Начало периода освоения"))
    period_end = models.DateField(_("Конец периода освоения"))

    class Meta:
        verbose_name = 'модуль программы'
        verbose_name_plural = 'модули программы'


class TargetModules(ObjectBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    target = models.ForeignKey("TrainingTarget")
    program_module = models.ForeignKey("ProgramModules")
    choice_group = models.ForeignKey("ChoiceGroup")

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

    def get_modules(self):
        program_modules = ProgramModules.objects.filter(program=self.program, choice_group=self)
        return [program_module.module.id for program_module in program_modules]


class ChoiceGroupType(ObjectBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('Наименование типы группы выбора'), blank=False, max_length=2048, default=_(''))

    class Meta:
        verbose_name = 'тип группы выбора'
        verbose_name_plural = 'типы группы выбора'

    def __str__(self):
        return self.title
