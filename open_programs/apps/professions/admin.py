from django.contrib import admin
from reversion.admin import VersionAdmin

from django.utils.translation import ugettext_lazy as _

from .models import Profession

@admin.register(Profession)
class ProfessionAdmin(VersionAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'archived'),
            'description': _("Профессия публикуется автоматически!")
        }),
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