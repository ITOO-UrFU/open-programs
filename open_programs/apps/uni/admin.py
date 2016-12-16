from django.contrib import admin

from .models import Qualification, Speciality


class QualificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
admin.site.register(Qualification, QualificationAdmin)


class SpecialityAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uid',
        'okso',
        'title',
        'ministerialCode',
        'ugnTitle',
        'standard',
    )
    raw_id_fields = ('qualifications',)
admin.site.register(Speciality, SpecialityAdmin)