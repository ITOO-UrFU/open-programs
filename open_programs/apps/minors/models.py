from django.utils.translation import ugettext_lazy as _

from django.db import models
from base.models import ObjectBaseClass
from courses.models import Course

import uuid


class Minor(ObjectBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("Название майнора"), max_length=256, blank=False, default=_("Название майнора"))
    description = models.TextField(_("Описание майнора"), max_length=16384, blank=True, default="")
    courses = models.ManyToManyField(Course, verbose_name=_("Варианты реализации майнора"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'майнор'
        verbose_name_plural = 'майноры'

    def get_all_courses(self):
        return "\n".join([str(course)for course in self.courses.all()])

class MinorsPool(ObjectBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("Название пула майноров"), max_length=256, blank=False, default=_("Название пула"))
    description = models.TextField(_("Описание"), max_length=16384, blank=True, default="")
    modules = models.ManyToManyField(Minor)

    def get_all(self):
        return "\n".join([str(module)for module in self.modules.all()])

    class Meta:
        verbose_name = 'пул майноров'
        verbose_name_plural = 'пулы майноров'