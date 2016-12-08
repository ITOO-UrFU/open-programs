from django.contrib import admin
from django.db import models
from reversion.admin import VersionAdmin
from codemirror2.widgets import CodeMirrorEditor

from .models import Course, Session


@admin.register(Course)
class CourseAdmin(VersionAdmin):

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.attname in ("description", "about"):
            kwargs['widget'] = CodeMirrorEditor(options={'mode': 'htmlmixed', 'lineNumbers': True, 'lineWrapping': True},
                                                modes=['css', 'xml', 'javascript', 'htmlmixed'],
                                                )
        return super(CourseAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    fields = ("title", "slug", "description", "about", "staff", "cover", "video", "video_cover", "workload", "points", "duration", "sessions", "results", "results_text", "status", "archived")
    list_display = ("title", "slug", "short_description", "short_about", "get_cover", "video", "video_cover", "workload", "points", "duration", "status", "archived", "all_sessions_colors")
    filter_horizontal = ("sessions", "staff", "results")
    list_filter = ('archived', 'created', 'updated')
    search_fields = ('slug', "title")



@admin.register(Session)
class SessionAdmin(VersionAdmin):
    fields = ("slug", "startdate", "enddate")
    list_display = ("slug", "startdate", "enddate")
    list_filter = ('startdate', 'enddate')
    search_fields = ('slug', )