from django.db.models import Q
from django.utils.html import escape
from .models import Discipline, Semester
from programs.models import Program
from ajax_select import LookupChannel


class DisciplineLookup(LookupChannel):

    model = Discipline

    @classmethod
    def get_query(cls, q, request):
        return Discipline.objects.filter(Q(title__icontains=q) | Q(uni_number__icontains=q) | Q(uni_uid__icontains=q), Q(status="p") & Q(archived=False)).order_by('title')

    @classmethod
    def get_result(cls, obj):
        """ result is the simple text that is the completion of what the person typed """
        return str(obj)

    @classmethod
    def format_match(cls, obj):
        """ (HTML) formatted item for display in the dropdown """
        return escape(str(obj))

    @classmethod
    def format_item_display(cls, obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return f"{obj.title} - {obj.labor} з.е.<br /><span style='font-size: 0.9em;padding-left: 1.5em;color: grey;'>" \
               f"{obj.module.uni_coordinator}</span>"


class SemesterLookup(LookupChannel):

    model = Semester


    def get_query(self, q, request):
        return Semester.objects.filter(Q(discipline__title__icontains=q) | Q(discipline__uni_number__icontains=q) | Q(discipline__uni_uid__icontains=q), Q(discipline__status="p") & Q(discipline__archived=False))

    def get_result(self, obj):
        """ result is the simple text that is the completion of what the person typed """
        return str(obj)

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return escape(f"{obj.discipline.title} - {obj.term}")

    def format_item_display(self, obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return f"{obj.discipline.title} - {obj.term}<br /><span style='font-size: 0.9em;padding-left: 1.5em;color: grey;'>" \
               f"{obj.discipline.module.uni_coordinator}</span>"

