from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Person


@admin.register(Person)
class CourseAdmin(VersionAdmin):
    fields = ("user", "first_name", "second_name", "last_name", "sex", "alt_email", "country", "birthday_date", "biography")
    list_display = ("user", "first_name", "second_name", "last_name", "sex", "alt_email", "country", "birthday_date", "biography")
    list_filter = ('first_name', 'second_name', 'last_name', "user")
    search_fields = ('user', "first_name", "second_name", "last_name")