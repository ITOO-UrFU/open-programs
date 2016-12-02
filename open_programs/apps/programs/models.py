import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from modules.models import Module, ModulesPool, ChoicePool


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

    general_base_modules = models.ManyToManyField(Module, verbose_name=_("Общепрофессиональные базовые модули"))
    educational_program_trajectories = models.ManyToManyField(ModulesPool, verbose_name=_("Траектория образовательной программы"))
    choice_pool = models.ManyToManyField(ChoicePool, verbose_name=_("Пул модулей по выбору"))

