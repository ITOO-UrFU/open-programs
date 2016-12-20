from django.db import models
from base.models import ObjectBaseClass
from results.models import Result

from permission import add_permission_logic
from permission.logics import StaffPermissionLogic

from django.utils.translation import ugettext_lazy as _


class Competence(ObjectBaseClass):
    title = models.CharField(_("Компетенция"), max_length=512, blank=False, default=_(""))
    results = models.ManyToManyField(Result, verbose_name=_("Результаты обучения"))
    profession = models.ForeignKey("professions.Profession", blank=True, null=True)

    class Meta:
        verbose_name = 'компетенция'
        verbose_name_plural = 'компетенции'

    def __str__(self):
        return str(self.title)

add_permission_logic(Competence, StaffPermissionLogic())