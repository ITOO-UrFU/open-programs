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
    type = models.ForeignKey("Type", verbose_name="Тип модуля", default=0, null=True)
    results = models.ManyToManyField(Result, verbose_name=_("Результаты обучения"), blank=True)
    results_text = models.TextField(_("Результаты обучения"), max_length=16384, blank=True, default="")
    competences = models.ManyToManyField(Competence, verbose_name=_("Компетенции"), blank=True)
    semester = models.PositiveIntegerField(_("Семестр"), blank=True, null=True)

    def get_all_disciplines(self):
        return Discipline.objects.filter(module__id=self.id)

    class Meta:
        verbose_name = 'модуль'
        verbose_name_plural = 'модули'

    def __str__(self):
        return self.title
