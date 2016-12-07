from django.db import models
from base.models import ObjectBaseClass

from permission import add_permission_logic
from permission.logics import StaffPermissionLogic

from django.utils.translation import ugettext_lazy as _


class Competence(ObjectBaseClass):
    title = models.CharField(_("Компетенция"), max_length=512, blank=False, default=_(""))
    #  todo: add results m2m
    def __str__(self):
        return str(self.title)

add_permission_logic(Competence, StaffPermissionLogic())