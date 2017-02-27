from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Program, TrainingTarget, ProgramCompetence, ProgramModules, TargetModules, ChoiceGroup, ChoiceGroupType


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
    list_filter = ('title', 'chief', "training_direction", "level", 'created', 'updated', 'status', 'archived',)
    # filter_horizontal = (
    #     'program_modules',
    # )


@admin.register(TrainingTarget)
class TrainingTargetAdmin(VersionAdmin):
    list_display = (
        "title",
        "number"
    )  # TODO: "program"
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


@admin.register(ProgramModules)
class ProgramModulesAdmin(VersionAdmin):
    list_display = ("id",  "semester", "module", "program", "choice_group", "competence")
    list_filter = ("program", "period_start", "period_end")
    raw_id_fields = ("module", )


@admin.register(TargetModules)
class TargetModulesAdmin(VersionAdmin):
    list_display = ("id", )  # TODO: "choice_group", "program_module", "target"


@admin.register(ChoiceGroup)
class ChoiceGroupAdmin(VersionAdmin):
    list_display = ("id", "program", "title", "labor", "choice_group_type", "number")


@admin.register(ChoiceGroupType)
class ChoiceGroupTypeAdmin(VersionAdmin):
    list_display = ("title", )