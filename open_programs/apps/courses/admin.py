from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Course


@admin.register(Course)
class CourseAdmin(VersionAdmin):
    fields = ("title", "slug", "description", "about", "cover", "video", "video_cover", "workload", "points", "duration", "status", "archived")
    list_display = ("title", "slug", "description", "about", "cover", "video", "video_cover", "workload", "points", "duration", "status", "archived")