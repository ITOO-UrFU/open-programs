from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Program

@admin.register(Program)
class ProgramAdmin(VersionAdmin):
    fields = ("title", "chief", "general_base_modules", "educational_program_trajectories", "choice_modules",  "status", "archived")
    list_display = ("title", "chief", "get_all_general_base_modules", "get_all_educational_program_trajectories", "get_all_choice_modules", "status", "archived")