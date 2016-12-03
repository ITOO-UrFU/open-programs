import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from modules.models import Module, GeneralBaseModulesPool, EducationalProgramTrajectoriesPool, ChoiceModulesPool
from persons.models import Person

class Program(models.Model):
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
    chief = models.OneToOneField(Person, blank=True, null=True)

    #general_base_modules = models.ManyToManyField(GeneralBaseModulesPool, verbose_name=_("Общепрофессиональные базовые модули"))
    #educational_program_trajectories = models.ManyToManyField(EducationalProgramTrajectoriesPool, verbose_name=_("Траектория образовательной программы"))
    #choice_modules = models.ManyToManyField(ChoiceModulesPool, verbose_name=_("Пул модулей по выбору"))

    #def get_all_general_base_modules(self):
        #return "\n".join([str(module)for module in self.GeneralBaseModulesPool.all()])

    #def get_all_educational_program_trajectories(self):
        #return "\n".join([str(module)for module in self.EducationalProgramTrajectoriesPool.all()])

    #def get_all_choice_modules(self):
        #return "\n".join([str(module)for module in self.ChoiceModulesPool.all()])