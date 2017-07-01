from django.db.models import Q
from django.utils.html import escape
from .models import Module
from ajax_select import LookupChannel


class ModuleLookup(LookupChannel):

    model = Module

    @classmethod
    def get_query(cls, q, request):
        return Module.objects.filter(Q(title__icontains=q) | Q(uni_number__icontains=q) | Q(uni_uid__icontains=q), Q(status="p") & Q(archived=False)).order_by('title')

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
        return f"{obj.title} - {obj.uni_number} з.е.<br /><span style='font-size: 0.9em;padding-left: 1.5em;color: grey;'>" \
               f"{obj.uni_coordinator}</span>"
