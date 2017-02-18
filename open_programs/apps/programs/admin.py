from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Program, TrainingTarget, ProgramCompetence


@admin.register(Program)
class ProgramAdmin(VersionAdmin):
    list_display = (
        'title',
        "training_direction",
        'chief',
        "level",
        'created',
        'updated',
        'archived',
        'status',

    )
    list_filter = ('title', 'chief', "training_direction", "level", "program_modules", 'created', 'updated', 'status', 'archived',)
    filter_horizontal = (
        'program_modules',
    )


@admin.register(TrainingTarget)
class TrainingTargetAdmin(VersionAdmin):
    list_display = (
        "title",
        "program",
        "number"
    )
    list_filter = (
        "title",
        "program",
        "number"
    )
    filter_horizontal = ("program", )


@admin.register(ProgramCompetence)
class ProgramCompetenceAdmin(VersionAdmin):
    list_display = ("title", "number")
    list_filter = ("title", "number")
    search_fields = ("title", )
