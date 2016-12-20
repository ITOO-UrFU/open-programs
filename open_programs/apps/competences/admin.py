from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Competence
from results.models import Result


class ResultInline(admin.StackedInline):
    model = Competence.results.through


@admin.register(Competence)
class CompetenceAdmin(VersionAdmin):
    list_display = (
        "title",
        "profession",
        "archived",
        "created",
        "updated",
        "status",
    )
    list_filter = ("archived", "created", "updated")
    exclude = ("results", )
    inlines = [ResultInline, ]
