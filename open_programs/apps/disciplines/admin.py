from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Discipline


@admin.register(Discipline)
class DisciplineAdmin(VersionAdmin):
    fields = ("name", "courses", "status", "archived", "results", "results_text")
    list_display = ("name", "get_all", "status", "archived")