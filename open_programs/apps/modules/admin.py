from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Module, GeneralBaseModulesPool, EducationalProgramTrajectoriesPool, ChoiceModulesPool, Type


@admin.register(Module)
class ModuleAdmin(VersionAdmin):
    fields = ("title",
              "description",
              "status",
              "archived",
              "type",
              "results",
              "results_text",
              "competences"
              )

    list_display = ("id", "title", "description", "status", "archived", "type") #"get_all_disciplines",
    filter_horizontal = ("results", "competences")
    list_filter = ('archived', 'created', 'updated', 'type')


@admin.register(GeneralBaseModulesPool)
class GeneralBaseModulesPoolAdmin(VersionAdmin):
    fields = ("title", "description", "modules", "status", "archived")
    list_display = ("id", "title", "description", "get_all", "status", "archived")
    list_filter = ('archived', 'created', 'updated')
    filter_horizontal = ("modules", )


@admin.register(EducationalProgramTrajectoriesPool)
class EducationalProgramTrajectoriesPoolAdmin(VersionAdmin):
    fields = ("title", "description", "modules", "status", "archived")
    list_display = ("id", "title", "description", "get_all", "status", "archived")
    list_filter = ('archived', 'created', 'updated')
    filter_horizontal = ("modules", )


@admin.register(ChoiceModulesPool)
class ChoiceModulesPoolAdmin(VersionAdmin):
    fields = ("title", "description", "modules", "status", "archived")
    list_display = ("id", "title", "description", "get_all", "status", "archived")
    list_filter = ('archived', 'created', 'updated')
    filter_horizontal = ("modules", )


@admin.register(Type)
class TypeAdmin(VersionAdmin):
    fields = ("title", "description")
    list_display = ("id", "title", "description")
    list_filter = ("archived", "created", "updated")