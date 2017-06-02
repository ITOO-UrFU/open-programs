from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Module, Type


@admin.register(Module)
class ModuleAdmin(VersionAdmin):
    list_display = ("title", "program", "uni_uuid", "semester", "status", "archived", "type") #"get_all_disciplines",
    filter_horizontal = ("results", "competences")
    list_filter = ('archived', "semester", 'created', 'updated', 'type')
    search_fields = ("title", "uni_number", "uni_uuid")


@admin.register(Type)
class TypeAdmin(VersionAdmin):
    fields = ("title", "description")
    list_display = ("id", "title", "description")
    list_filter = ("archived", "created", "updated")