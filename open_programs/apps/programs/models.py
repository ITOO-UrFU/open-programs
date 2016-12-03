import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from modules.models import Module, GeneralBaseModulesPool, EducationalProgramTrajectoriesPool, ChoiceModulesPool
from minors.models import Minor


class ObjectBaseClass(models.Model):
    class Meta:
        abstract = True

    STATUSES = (
        ('h', _("Скрыт")),
        ('p', _("Опубликован")),
    )
    archived = models.BooleanField(_("В архиве"), default=False)
    created = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated = models.DateTimeField(_('Обновлен'), auto_now=True)
    status = models.CharField(_("Статус публикации"), max_length=1, choices=STATUSES, default='h')


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

    general_base_modules = models.ManyToManyField(GeneralBaseModulesPool, verbose_name=_("Общепрофессиональные базовые модули"))
    educational_program_trajectories = models.ManyToManyField(EducationalProgramTrajectoriesPool, verbose_name=_("Траектория образовательной программы"))
    choice_modules = models.ManyToManyField(ChoiceModulesPool, verbose_name=_("Пул модулей по выбору"))


    def minors(self):
        return Minor.objects.filter(archived=False, status="p")


