from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Program

# @admin.register(Program)
# class ProgramAdmin(VersionAdmin):
#     fields = ("title", "chief", "general_base_modules", "educational_program_trajectories", "choice_modules",  "status", "archived")
#     list_display = ("title", "chief", "get_all_general_base_modules", "get_all_educational_program_trajectories", "get_all_choice_modules", "status", "archived")
#


class ProgramAdmin(VersionAdmin):
    list_display = (
        'title',
        'chief',
        'created',
        'updated',
        'archived',
        'status',

    )
    list_filter = ('title', 'chief', 'created', 'updated', 'status', 'archived',)
    filter_horizontal = (
        'general_base_modules',
        'educational_program_trajectories',
        'choice_modules',
    )
admin.site.register(Program, ProgramAdmin)