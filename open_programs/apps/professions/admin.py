from django.contrib import admin

from reversion.admin import VersionAdmin

from django.utils.translation import ugettext_lazy as _

from .models import Profession
from competences.models import Competence


@admin.register(Profession)
class ProfessionAdmin(VersionAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'archived'),
            'description': _("Профессия публикуется автоматически!")
        }),
        #("Требования", {'fields': ("competences",)})
    )
    list_display = (
        "title",
        "description",
        "archived",
        "created",
        "updated",
        "status",
    )
    list_filter = ("archived", "created", "updated")
