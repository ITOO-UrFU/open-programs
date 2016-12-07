from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Module, GeneralBaseModulesPool, EducationalProgramTrajectoriesPool, ChoiceModulesPool, Type


@admin.register(Module)
class ModuleAdmin(VersionAdmin):
    fields = ("title", "description", "disciplines", "status", "archived", "type")
    list_display = ("id", "title", "description", "get_all_disciplines", "status", "archived", "type")
    list_filter = ('archived', 'created', 'updated', 'type')


@admin.register(GeneralBaseModulesPool)
class GeneralBaseModulesPoolAdmin(VersionAdmin):
    fields = ("title", "description", "modules", "status", "archived")
    list_display = ("id", "title", "description", "get_all", "status", "archived")
    list_filter = ('archived', 'created', 'updated')


@admin.register(EducationalProgramTrajectoriesPool)
class EducationalProgramTrajectoriesPoolAdmin(VersionAdmin):
    fields = ("title", "description", "modules", "status", "archived")
    list_display = ("id", "title", "description", "get_all", "status", "archived")
    list_filter = ('archived', 'created', 'updated')


@admin.register(ChoiceModulesPool)
class ChoiceModulesPoolAdmin(VersionAdmin):
    fields = ("title", "description", "modules", "status", "archived")
    list_display = ("id", "title", "description", "get_all", "status", "archived")
    list_filter = ('archived', 'created', 'updated')


@admin.register(Type)
class TypeAdmin(VersionAdmin):
    fields = ("title", "description")
    list_display = ("id", "title", "description")
    list_filter = ("archived", "created", "updated")