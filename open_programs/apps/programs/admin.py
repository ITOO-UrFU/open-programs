from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Program


@admin.register(Program)
class ProgramAdmin(VersionAdmin):
    fields = ("title", "chief")
    list_display = ("title", "chief")