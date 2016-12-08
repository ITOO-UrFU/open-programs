from django.db import models
from base.models import ObjectBaseClass
from django.utils.translation import ugettext_lazy as _

from courses.models import Course
from results.models import Result

class Discipline(ObjectBaseClass):
    name = models.CharField(_('Название дисциплины'), max_length=256, blank=False, default='')
    courses = models.ManyToManyField(Course, verbose_name=_("Варианты реализации дисциплины"))
    results = models.ManyToManyField(Result, verbose_name=_("Результаты обучения"))
    results_text = models.TextField(_("Результаты обучения"), max_length=16384, blank=True, default="")

    class Meta:
        verbose_name = 'дисциплина'
        verbose_name_plural = 'дисциплины'

    def __str__(self):
        return self.name

    def get_all(self):
        return "\n".join([str(course)for course in self.courses.all()])