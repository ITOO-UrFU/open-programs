import uuid

from django.db import models
from base.models import ObjectBaseClass
from django.utils.translation import ugettext_lazy as _

from modules.models import Module, GeneralBaseModulesPool, EducationalProgramTrajectoriesPool, ChoiceModulesPool
from persons.models import Person


class Program(ObjectBaseClass):
    """
    Чё у нас тут есть:
    - общепрофессиональные базовые модули
    - траектория образовательной программы
    - модули по выбору
    - майноры
    - всякая практика, которой пока нет
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(_('Название образовательной программы'), blank=False, max_length=256, default=_(''))
    chief = models.OneToOneField(Person, verbose_name=_('Руководитель образовательной программы'), blank=False, null=True)

    general_base_modules = models.ManyToManyField(GeneralBaseModulesPool, verbose_name=_("Общепрофессиональные базовые модули"))
    educational_program_trajectories = models.ManyToManyField(EducationalProgramTrajectoriesPool, verbose_name=_("Траектории образовательной программы"))
    choice_modules = models.ManyToManyField(ChoiceModulesPool, verbose_name=_("Пул модулей по выбору"))
    module_dependencies = models.ManyToManyField("ModuleDependency", verbose_name=_("Зависимости модулей"))

    def get_all_general_base_modules(self):
        return "\n".join([str(module)for module in self.general_base_modules.all()])

    def get_all_educational_program_trajectories(self):
        return "\n".join([str(module)for module in self.educational_program_trajectories.all()])

    def get_all_choice_modules(self):
        return "\n".join([str(module)for module in self.choice_modules.all()])

    class Meta:
        verbose_name = 'программа'
        verbose_name_plural = 'программы'


class ModuleDependency(models.Model):
    DEPENDENCY_TYPES = (
        ("soft", _("мягкая")),
        ("hard", _("строгая")),
    )
    module = models.ForeignKey(Module, related_name="module")
    dependencies = models.ManyToManyField(Module, related_name="modules")
    type = models.CharField(_("Тип зависимости"), max_length=4, default="hard", choices=DEPENDENCY_TYPES)

    class Meta:
        verbose_name = 'зависимость'
        verbose_name_plural = 'зависимости'

    def __str__(self):
        return self.type + '-' + str(self.module) + "-" + "-".join([str(module) for module in self.dependencies])
