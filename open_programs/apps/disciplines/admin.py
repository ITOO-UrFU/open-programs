from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Discipline


@admin.register(Discipline)
class DisciplineAdmin(VersionAdmin):
    fields = ("name", "description", "courses", "module", "points", "form", "status", "archived", "results", "results_text")
    list_display = ("name", "description", "module", "get_all", "points", "form", "status", "archived")
    filter_horizontal = ("courses", "results")
    list_filter = ("archived", "created", "updated", "status", "form")