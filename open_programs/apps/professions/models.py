from django.db import models
from base.models import ObjectBaseClass
from competences.models import Competence

from permission import add_permission_logic
from permission.logics import StaffPermissionLogic

from django.utils.translation import ugettext_lazy as _


class Profession(ObjectBaseClass):
    title = models.CharField(_("Название профессии"), max_length=256, blank=False, default=_(""))
    description = models.TextField(_("Описание профессии"), max_length=16384, blank=True, default=_("Здесь должно быть описание профессии"))
    #competences = models.ManyToManyField(Competence, verbose_name=_("Компетенции"))

    def competences(self):
        return Competence.objects.filter(profession__id=self.id)

    def save(self, *args, **kwargs):
        self.status = "p"
        super(Profession, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'профессия'
        verbose_name_plural = 'профессии'

    def __str__(self):
        return str(self.title)

    @models.permalink
    @classmethod
    def get_absolute_url(self):
        return None

add_permission_logic(Profession, StaffPermissionLogic())