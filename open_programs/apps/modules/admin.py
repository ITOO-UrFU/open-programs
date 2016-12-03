from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Module, GeneralBaseModulesPool, EducationalProgramTrajectoriesPool, ChoiceModulesPool


@admin.register(Module)
class ModuleAdmin(VersionAdmin):
    fields = ("title", "description")
    list_display = ("id", "title", "description")


@admin.register(GeneralBaseModulesPool)
class GeneralBaseModulesPoolAdmin(VersionAdmin):
    fields = ("title", "description", "modules")
    list_display = ("id", "title", "description", "get_all")


@admin.register(EducationalProgramTrajectoriesPool)
class EducationalProgramTrajectoriesPoolAdmin(VersionAdmin):
    fields = ("title", "description", "modules")
    list_display = ("id", "title", "description", "get_all")


@admin.register(ChoiceModulesPool)
class ChoiceModulesPoolAdmin(VersionAdmin):
    fields = ("title", "description", "modules")
    list_display = ("id", "title", "description", "get_all")