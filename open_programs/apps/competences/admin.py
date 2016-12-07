from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Competence


@admin.register(Competence)
class CompetenceAdmin(VersionAdmin):
    list_display = (
        "title",
        "archived",
        "created",
        "updated",
        "status",
    )
    list_filter = ("archived", "created", "updated")
    filter_horizontal = ("results", )
