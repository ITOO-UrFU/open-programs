from django.db import models
from base.models import ObjectBaseClass
from django.utils.translation import ugettext_lazy as _

from courses.models import Course
from results.models import Result


class Discipline(ObjectBaseClass):
    FORMS = (
        ('e', _('Экзамен')),
        ('z', _('Зачет'))
        )
    name = models.CharField(_('Название дисциплины'), max_length=256, blank=False, default='')
    description = models.TextField(_("Короткое описание"), max_length=16384, blank=True, null=True)
    module = models.ForeignKey("modules.Module", blank=True, null=True)
    points = models.PositiveIntegerField(_("зачётных единиц"), blank=False, default=0)
    courses = models.ManyToManyField(Course, verbose_name=_("Варианты реализации дисциплины"), blank=True)
    form = models.CharField(_("Форма контроля"), max_length=1, choices=FORMS, default='z')
    results = models.ManyToManyField(Result, verbose_name=_("Результаты обучения"), blank=True)
    results_text = models.TextField(_("Результаты обучения"), max_length=16384, blank=True, default="")

    class Meta:
        verbose_name = 'дисциплина'
        verbose_name_plural = 'дисциплины'

    def __str__(self):
        return self.name

    def get_all(self):
        return "\n".join([str(course)for course in self.courses.all()])