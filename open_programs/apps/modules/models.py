from django.db import models
from base.models import ObjectBaseClass
from django.utils.translation import ugettext_lazy as _
import uuid

from results.models import Result
from competences.models import Competence
from disciplines.models import Discipline


class Type(ObjectBaseClass):
    title = models.CharField(_("Название типа модуля"), max_length=256, blank=False, default=_("Название типа модуля"))
    description = models.TextField(_("Описание"), max_length=16384, blank=True, default="")

    class Meta:
        verbose_name = 'тип модуля'
        verbose_name_plural = 'типы модулей'

    def __str__(self):
        return self.title


class Module(ObjectBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("Название модуля"), max_length=256, blank=False)
    description = models.TextField(_("Описание модуля"), max_length=16384, blank=True, default="")
    #disciplines = models.ManyToManyField(Discipline, verbose_name=_("Дисциплины"), blank=True)
    type = models.ForeignKey("Type", verbose_name="Тип модуля", default=0, null=True)
    results = models.ManyToManyField(Result, verbose_name=_("Результаты обучения"), blank=True)
    results_text = models.TextField(_("Результаты обучения"), max_length=16384, blank=True, default="")
    competences = models.ManyToManyField(Competence, verbose_name=_("Компетенции"), blank=True)

    def get_all_disciplines(self):
        return Discipline.objects.filter(module__id=self.id)

    class Meta:
        verbose_name = 'модуль'
        verbose_name_plural = 'модули'

    def __str__(self):
        return self.title


class GeneralBaseModulesPool(ObjectBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("Название базового модуля программы"), max_length=256, blank=False, default=_("Название пула"))
    description = models.TextField(_("Описание"), max_length=16384, blank=True, default="")
    modules = models.ManyToManyField(Module, verbose_name=_("модули"))

    class Meta:
        verbose_name = 'базовый модуль программы'
        verbose_name_plural = 'базовые модули программы'

    def get_all(self):
        return "\n".join([str(module)for module in self.modules.all()])

    def __str__(self):
        return self.title


class EducationalProgramTrajectoriesPool(ObjectBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("Название пула модулей траектории обр. программ"), max_length=256, blank=False, default=_("Название пула"))
    description = models.TextField(_("Описание"), max_length=16384, blank=True, default="")
    modules = models.ManyToManyField(Module, verbose_name=_("модули"))

    class Meta:
        verbose_name = 'пул модулей траектории обр. программ'
        verbose_name_plural = 'пулы модулей траектории обр. программ'

    def get_all(self):
        return "\n".join([str(module)for module in self.modules.all()])

    def __str__(self):
        return self.title


class ChoiceModulesPool(ObjectBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("Название пула модулей по выбору"), max_length=256, blank=False, default=_("Название пула"))
    description = models.TextField(_("Описание"), max_length=16384, blank=True, default="")
    modules = models.ManyToManyField(Module, verbose_name=_("модули"))

    class Meta:
        verbose_name = 'пул модулей по выбору'
        verbose_name_plural = 'пулы модулей по выбору'

    def get_all(self):
        return "\n".join([str(module)for module in self.modules.all()])

    def __str__(self):
        return self.title