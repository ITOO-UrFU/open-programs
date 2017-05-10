from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Discipline, TrainingTerms, Semester


@admin.register(Discipline)
class DisciplineAdmin(VersionAdmin):
    fields = ("title", "description", "courses", "module", "period",  "labor", "form", "status", "archived", "results", "results_text")
    list_display = ("id", "title", "description", "module", "get_all", "period", "labor", "form", "status", "archived")
    filter_horizontal = ("courses", "results")
    list_filter = ("archived", "created", "updated", "status", "form")
    search_fields = ['title', 'module__title', "module__uni_number"]


@admin.register(TrainingTerms)
class TrainingTermsAdmin(VersionAdmin):
    list_display = ("title", "limit")


@admin.register(Semester)
class SemesterAdmin(VersionAdmin):
    list_display = ("__str__", )
