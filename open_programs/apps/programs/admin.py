from django.contrib import admin
from reversion.admin import VersionAdmin
from ajax_select.admin import AjaxSelectAdmin
from ajax_select import make_ajax_form

from .models import Program, TrainingTarget, ProgramCompetence, ProgramModules, TargetModules, ChoiceGroup, ChoiceGroupType, LearningPlan, StudentProgram


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
    list_filter = ("level", 'created', 'updated', 'status', 'archived',)
    filter_horizontal = ("learning_plans", )


@admin.register(TrainingTarget)
class TrainingTargetAdmin(VersionAdmin):
    list_display = (
        "title",
        "number"
    )  # TODO: "program"
    list_filter = (
        "program",
        "number"
    )


@admin.register(ProgramCompetence)
class ProgramCompetenceAdmin(VersionAdmin):
    list_display = ("title", "number", "program", "color")
    list_filter = ("title", "number", "color")
    search_fields = ("title", )


@admin.register(ProgramModules)
class ProgramModulesAdmin(VersionAdmin):
    list_display = ("id",  "semester", "module", "program", "choice_group", "competence")
    list_filter = ("program", "semester",)
    raw_id_fields = ("module", )


@admin.register(TargetModules)
class TargetModulesAdmin(VersionAdmin):
    list_display = ("id", )  # TODO: "choice_group", "program_module", "target"


@admin.register(ChoiceGroup)
class ChoiceGroupAdmin(VersionAdmin, AjaxSelectAdmin):
    list_display = ("id", "program", "title", "labor", "choice_group_type", "number")
    # form = make_ajax_form(ChoiceGroup, {'program': 'program'})
    save_as = True


@admin.register(ChoiceGroupType)
class ChoiceGroupTypeAdmin(VersionAdmin):
    list_display = ("title", )


@admin.register(LearningPlan)
class LearningPlanAdmin(VersionAdmin):
    list_display = ('uni_displayableTitle', 'uni_number', 'uni_title', 'uni_stage', 'uni_loadTimeType')


@admin.register(StudentProgram)
class StudentProgramAdmin(VersionAdmin):
    list_display = ("link", "program", "user")
    fields = ("link", "user", "program", "json")
    readonly_fields = ("link", )
