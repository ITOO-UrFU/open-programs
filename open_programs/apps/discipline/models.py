from django.db import models
from base.models import ObjectBaseClass
from django.utils.translation import ugettext_lazy as _

from courses.models import Course


class Discipline(ObjectBaseClass):
    name = models.CharField(_('Название дисциплины'), max_length=256, blank=False, default='')
    courses = models.ManyToManyField(Course, verbose_name=_("Варианты реализации дисциплины"))

    class Meta:
        verbose_name = 'дисциплина'
        verbose_name_plural = 'дисциплины'

    def __str__(self):
        return self.name

    def get_all(self):
        return "\n".join([str(course)for course in self.courses.all()])