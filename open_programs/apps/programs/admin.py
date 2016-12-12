from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Program, ModuleDependency


@admin.register(Program)
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


@admin.register(ModuleDependency)
class ModuleDependencyAdmin(VersionAdmin):
    list_display = ('id', 'module', 'type')
    list_filter = ('module',)
    filter_horizontal = ('dependencies',)  # TODO: list modules from program!!!?
