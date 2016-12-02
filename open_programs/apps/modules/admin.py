from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Module, ModulesPool, ChoicePool


@admin.register(Module)
class ModuleAdmin(VersionAdmin):
    fields = ("title", "description")
    list_display = ("id", "title", "description")


@admin.register(ModulesPool)
class ModulesPoolAdmin(VersionAdmin):
    fields = ("title", "description", "modules")
    list_display = ("id", "title", "description", "get_all")


@admin.register(ChoicePool)
class ChoicePoolAdmin(VersionAdmin):
    fields = ("title", "description", "modules")
    list_display = ("id", "title", "description", "get_all")