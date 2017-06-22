from django.db import models
from django.db.models import Sum
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
    type = models.ForeignKey("Type", verbose_name="Тип модуля", default=1, null=True)
    results = models.ManyToManyField(Result, verbose_name=_("Результаты обучения"), blank=True)
    results_text = models.TextField(_("Результаты обучения"), max_length=16384, blank=True, default="")
    competences = models.ManyToManyField(Competence, verbose_name=_("Компетенции"), blank=True)
    semester = models.PositiveIntegerField(_("Семестр"), blank=True, null=True)
    program = models.ForeignKey("programs.Program", blank=True, null=True)

    uni_uuid = models.CharField(max_length=265, null=True, blank=True)
    uni_number = models.IntegerField(null=True, blank=True)
    uni_coordinator = models.CharField(max_length=265, null=True, blank=True)
    uni_type = models.CharField(max_length=265, null=True, blank=True)
    uni_title = models.CharField(max_length=265, null=True, blank=True)
    uni_competence = models.CharField(max_length=265, null=True, blank=True)
    uni_testUnits = models.IntegerField(null=True, blank=True)
    uni_priority = models.IntegerField(null=True, blank=True)
    uni_state = models.CharField(max_length=265, null=True, blank=True)
    uni_approvedDate = models.CharField(max_length=265, null=True, blank=True)
    uni_comment = models.CharField(max_length=4096, null=True, blank=True)
    uni_file = models.CharField(max_length=265, null=True, blank=True)
    uni_specialities =models.TextField(null=True, blank=True)

    def get_all_disciplines(self):
        return Discipline.objects.filter(module=self)

    def get_all_discipline_ids(self):
        return [discipline.id for discipline in Discipline.objects.filter(module=self)]

    def get_all_discipline_custom(self):
        return [{"id": discipline.id,
                 "title": discipline.title,
                 "description": discipline.description,
                 "labor": discipline.labor,
                 "form": discipline.get_form_display()
                 } for discipline in Discipline.objects.filter(module=self, archived=False, status="p")]

    def get_labor(self):
        return Discipline.objects.filter(module=self, status="p", archived=False).aggregate(Sum('labor'))["labor__sum"]

    class Meta:
        verbose_name = 'модуль'
        verbose_name_plural = 'модули'

    def __str__(self):
        return self.title

    def get_type_display(self):
        return self.type.title


