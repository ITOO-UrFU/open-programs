from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Module, GeneralBaseModulesPool, EducationalProgramTrajectoriesPool, ChoiceModulesPool


@admin.register(Module)
class ModuleAdmin(VersionAdmin):
    fields = ("title", "description", "status", "archived")
    list_display = ("id", "title", "description", "status", "archived")


@admin.register(GeneralBaseModulesPool)
class GeneralBaseModulesPoolAdmin(VersionAdmin):
    fields = ("title", "description", "modules", "status", "archived")
    list_display = ("id", "title", "description", "get_all", "status", "archived")


@admin.register(EducationalProgramTrajectoriesPool)
class EducationalProgramTrajectoriesPoolAdmin(VersionAdmin):
    fields = ("title", "description", "modules", "status", "archived")
    list_display = ("id", "title", "description", "get_all", "status", "archived")


@admin.register(ChoiceModulesPool)
class ChoiceModulesPoolAdmin(VersionAdmin):
    fields = ("title", "description", "modules", "status", "archived")
    list_display = ("id", "title", "description", "get_all", "status", "archived")