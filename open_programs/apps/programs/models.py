import uuid

from django.db import models
from base.models import ObjectBaseClass
from django.utils.translation import ugettext_lazy as _

from modules.models import Module, GeneralBaseModulesPool, EducationalProgramTrajectoriesPool, ChoiceModulesPool
from persons.models import Person
from minors.models import Minor


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

    def get_all_general_base_modules(self):
        return "\n".join([str(module)for module in self.general_base_modules.all()])

    def get_all_educational_program_trajectories(self):
        return "\n".join([str(module)for module in self.educational_program_trajectories.all()])

    def get_all_choice_modules(self):
        return "\n".join([str(module)for module in self.choice_modules.all()])

    def minors(self):
        return "\n".join([str(m) for m in Minor.objects.filter(archived=False, status="p")])

    class Meta:
        verbose_name = 'программа'
        verbose_name_plural = 'программы'