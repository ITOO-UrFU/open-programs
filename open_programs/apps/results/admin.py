from django.contrib import admin
from reversion.admin import VersionAdmin

from django.utils.translation import ugettext_lazy as _

from .models import Result

@admin.register(Result)
class ResultAdmin(VersionAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'archived'),
            'description': _("Результаты обучения публикуется автоматически!")
        }),
    )
    list_display = (
        "title",
        "archived",
    )
    list_filter = ("archived", "created", "updated")