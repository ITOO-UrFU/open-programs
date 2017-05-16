from django.contrib import admin
from reversion.admin import VersionAdmin
from ajax_select.admin import AjaxSelectAdmin
from ajax_select import make_ajax_form

# from cms.admin import JSONEditor

from django.forms.widgets import Textarea
try:
    from django.forms.util import flatatt
except ImportError:
    from django.forms.utils import flatatt
from django.utils.safestring import mark_safe
from django.conf import settings
import json

from jsonfield import JSONField
from .models import Discipline, TrainingTerms, Semester, Variant, Technology, Diagram


class JSONEditor(Textarea):
    class Media:
        js = (
            getattr(settings, "JQUERY", settings.STATIC_URL + 'jquery-1.7.2.min.js'),
            getattr(settings, "JQUERY_UI", settings.STATIC_URL + 'jquery-ui.min.js'),
            getattr(settings, "JQUERY_EVENT_DRAG", settings.STATIC_URL + 'jquery.event.drag.js'),

            getattr(settings, "SLICK_JS_CORE", settings.STATIC_URL+'slickgrid/slick.core.js'),
            getattr(settings, "SLICK_JS_FORMATTERS", settings.STATIC_URL + 'slickgrid/slick.formatters.js'),
            getattr(settings, "SLICK_JS_EDITORS", settings.STATIC_URL + 'slickgrid/slick.editors.js'),
            getattr(settings, "SLICK_JS_GRID", settings.STATIC_URL + 'slickgrid/slick.grid.js'),
        )
        css = {'all': (getattr(settings, "SLICK_CSS", settings.STATIC_URL+'slickgrid/slick.grid.css'),)}

    def render(self, name, value, attrs=None):
        try:
            value = json.loads(value)
        except TypeError:
            pass
        input_attrs = {'hidden': True}
        input_attrs.update(attrs)
        if 'class' not in input_attrs:
            input_attrs['class'] = 'for_grideditor'
        else:
            input_attrs['class'] += ' for_grideditor'
        r = super(JSONEditor, self).render(name, value, input_attrs)
        div_attrs = {}
        div_attrs.update(attrs)
        div_attrs.update({'id': (attrs['id']+'_jsoneditor')})
        final_attrs = self.build_attrs(div_attrs, extra_attrs={"name": name})
        r += '''
        <script>

        document.addEventListener("DOMContentLoaded", function(event) {
                var grid;
                  var data = [];
                  var columns = [
                    {id: "1", name: "Нед. 1", field: "week1", width: 60, editor: Slick.Editors.Text},
                    {id: "2", name: "Нед. 2", field: "week2", width: 60, editor: Slick.Editors.Text},
                    {id: "3", name: "Нед. 3", field: "week3", width: 60, editor: Slick.Editors.Text},
                    {id: "4", name: "Нед. 4", field: "week4", width: 60, editor: Slick.Editors.Text},
                    {id: "5", name: "Нед. 5", field: "week5", width: 60, editor: Slick.Editors.Text},
                    {id: "6", name: "Нед. 6", field: "week6", width: 60, editor: Slick.Editors.Text},
                    {id: "7", name: "Нед. 7", field: "week7", width: 60, editor: Slick.Editors.Text},
                    {id: "8", name: "Нед. 8", field: "week8", width: 60, editor: Slick.Editors.Text},
                    {id: "9", name: "Нед. 9", field: "week9", width: 60, editor: Slick.Editors.Text},
                    {id: "10", name: "Нед. 10", field: "week10", width: 60, editor: Slick.Editors.Text},
                    {id: "11", name: "Нед. 11", field: "week11", width: 60, editor: Slick.Editors.Text},
                    {id: "12", name: "Нед. 12", field: "week12", width: 60, editor: Slick.Editors.Text},
                    {id: "13", name: "Нед. 13", field: "week13", width: 60, editor: Slick.Editors.Text},
                    {id: "14", name: "Нед. 14", field: "week14", width: 60, editor: Slick.Editors.Text},
                    {id: "15", name: "Нед. 15", field: "week15", width: 60, editor: Slick.Editors.Text},
                    {id: "16", name: "Нед. 16", field: "week16", width: 60, editor: Slick.Editors.Text},
                    {id: "17", name: "Нед. 17", field: "week17", width: 60, editor: Slick.Editors.Text},
                    {id: "18", name: "Нед. 18", field: "week18", width: 60, editor: Slick.Editors.Text},
                    {id: "19", name: "Нед. 19", field: "week19", width: 60, editor: Slick.Editors.Text},
                    {id: "20", name: "Нед. 20", field: "week20", width: 60, editor: Slick.Editors.Text},


                  ];
                  var options = {
                    editable: true,
                    enableAddRow: false,
                    enableCellNavigation: false,
                    asyncEditorLoading: false,
                    autoEdit: false
                  };

                grid = new Slick.Grid("#id_%(name)s_jsoneditor", data, columns, options);
                grid.setSelectionModel(new Slick.CellSelectionModel());
        });




        </script>
        <div %(attrs)s></div>
        ''' % {
            'attrs': flatatt(final_attrs),
            'name': name
        }
        return mark_safe(r)

@admin.register(Discipline)
class DisciplineAdmin(VersionAdmin):
    fields = ("title", "description", "module", "period",  "labor", "form", "status", "archived", "results", "results_text")
    list_display = ("id", "title", "description", "module", "period", "labor", "form", "status", "archived")
    filter_horizontal = ("results",)
    list_filter = ("archived", "created", "updated", "status", "form")
    search_fields = ['title', 'module__title', "module__uni_number"]


@admin.register(TrainingTerms)
class TrainingTermsAdmin(VersionAdmin):
    list_display = ("title", "limit")


@admin.register(Semester)
class SemesterAdmin(VersionAdmin):
    list_display = ("__str__", )
    search_fields = ("discipline__title", "discipline__module__title", "program__title")
    form = make_ajax_form(Semester, {'discipline': 'discipline'})


@admin.register(Variant)
class VariantAdmin(VersionAdmin, AjaxSelectAdmin):
    list_display = ("discipline", "program", "course", "semester", "parity", "link", "status", "archived")
    list_filter = ("parity", "archived", "created", "updated", "status")
    search_fields = ("discipline__title", "program__title", "course__title", "parity", "link")
    form = make_ajax_form(Variant, {'discipline': 'discipline'})


@admin.register(Technology)
class TechnologyAdmin(VersionAdmin):
    list_display = ("title", "description", "contact_work_category", "get_color")


@admin.register(Diagram)
class DiagramAdmin(VersionAdmin):
    list_display = ("title", "diagram")
    formfield_overrides = {
        JSONField: {'widget': JSONEditor},
    }
