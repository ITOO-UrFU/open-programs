from django.db.models import Q
from django.utils.html import escape
from .models import Program
from ajax_select import LookupChannel


class ProgramLookup(LookupChannel):

    model = Program

    def get_query(self, q, request):
        return Program.objects.filter(Q(title__icontains=q) | Q(training_direction__icontains=q), Q(status="p") & Q(archived=False)).order_by('title')

    def get_result(self, obj):
        """ result is the simple text that is the completion of what the person typed """
        return str(obj)

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return escape(str(obj))

    def format_item_display(self, obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return f"{obj.title}<br /><span style='font-size: 0.9em;padding-left: 1.5em;color: grey;'>" \
               f"{obj.training_direction}</span>"
