from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Course, Session


@admin.register(Course)
class CourseAdmin(VersionAdmin):
    fields = ("title", "slug", "description", "about", "cover", "video", "video_cover", "workload", "points", "duration", "sessions", "status", "archived")
    list_display = ("title", "slug", "description", "about", "cover", "video", "video_cover", "workload", "points", "duration", "status", "archived", "all_sessions_colors")
    filter_horizontal = ("sessions", )

@admin.register(Session)
class SessionAdmin(VersionAdmin):
    fields = ("slug", "startdate", "enddate")
    list_display = ("slug", "startdate", "enddate")