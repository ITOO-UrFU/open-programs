from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Module, Type


@admin.register(Module)
class ModuleAdmin(VersionAdmin):
    fields = ("title",
              "description",
              "semester",
              "status",
              "archived",
              "type",
              "results",
              "results_text",
              "competences"
              )

    list_display = ("id", "title", "description", "semester", "status", "archived", "type") #"get_all_disciplines",
    filter_horizontal = ("results", "competences")
    list_filter = ('archived', "semester", 'created', 'updated', 'type')


@admin.register(Type)
class TypeAdmin(VersionAdmin):
    fields = ("title", "description")
    list_display = ("id", "title", "description")
    list_filter = ("archived", "created", "updated")