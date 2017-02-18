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
    training_direction = models.CharField(_("Направление подготовки"), blank=False, max_length=256, default=_(''))  # TODO: obj or string?
    competences = models.ManyToManyField(Competence, blank=True)
    # choice_groups = models.ManyToManyField()
    chief = models.OneToOneField(Person, verbose_name=_('Руководитель образовательной программы'), blank=True, null=True)

    program_modules = models.ManyToManyField(Module, blank=True, verbose_name=_("Модули программы"))

    class Meta:
        verbose_name = 'программа'
        verbose_name_plural = 'программы'

    def __str__(self):
        return self.title


class TrainingTarget(ObjectBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('Наименование образовательной цели'), blank=False, max_length=256, default=_(''))
    program = models.ManyToManyField("Program")
    number = models.IntegerField(_("Порядковый номер цели"))
    
    
class ProgramCompetence(ObjectBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('Наименование компетенции'), blank=False, max_length=256, default=_(''))
    number = models.IntegerField(_("Номер компетенции"))


class ProgramModules(ObjectBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    program = models.ForeignKey("Program")
    module = models.ForeignKey("Module")
    # choice_group = models.ForeignKey()
    competence = models.ManyToManyField(Competence, blank=True)
    # period