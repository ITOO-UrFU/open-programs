from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Minor  # , MinorsPool


@admin.register(Minor)
class MinorAdmin(VersionAdmin):
    fields = ("title", "description", "courses", "status", "archived")
    list_display = ("id", "title", "description", "get_all_courses", "status", "archived")


# @admin.register(MinorsPool)
# class MinorsPoolAdmin(VersionAdmin):
#     fields = ("title", "description", "modules", "status", "archived")
#     list_display = ("id", "title", "description", "get_all", "status", "archived")