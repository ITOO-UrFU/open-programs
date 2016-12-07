from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Module, GeneralBaseModulesPool, EducationalProgramTrajectoriesPool, ChoiceModulesPool, Type


@admin.register(Module)
class ModuleAdmin(VersionAdmin):
<<<<<<< HEAD
    fields = ("title", "description", "discipliness", "status", "archived", "type", "dependencies")
=======
    fields = ("title", "description", "discipliness", "status", "archived", "type", "results", "results_text")
>>>>>>> a665de25527fd283f08450f261dfd7638874b23f
    list_display = ("id", "title", "description", "get_all_discipliness", "status", "archived", "type")
    filter_horizontal = ("dependencies", )
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