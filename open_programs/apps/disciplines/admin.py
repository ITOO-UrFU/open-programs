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
from .models import Discipline, TrainingTerms, Semester, Variant, Technology, Diagram, WorkingType


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
        data = []
        wts = WorkingType.objects.all()
        for i, wt in enumerate(wts):
            data.append({
                "wt": wt.title,
                "week1": 0,
                "week2": 0,
                "week3": 0,
                "week4": 0,
                "week5": 0,
                "week6": 0,
                "week7": 0,
                "week8": 0,
                "week9": 0,
                "week10": 0,
                "week11": 0,
                "week12": 0,
                "week13": 0,
                "week14": 0,
                "week15": 0,
                "week16": 0,
                "week17": 0,
                "week18": 0,
                "week19": 0,
                "week20": 0,
            })

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
        <style>
            .editor-text {{
                padding: 2px !important;
                margin: 0 !important;
                border-radius: 0px !important;
                width: 52px !important;
                border: none !important;
            }}
        </style>
        <script>

        document.addEventListener("DOMContentLoaded", function(event) {{
                var grid;
                var data = $("#id_diagram").val();
                //if (data.length < 10 ) {{
                //    data = {data}
                //}}
                  console.log(data);
                  var columns = [
                    {{id: "title", name: "Вид работы", field: "wt", width: 250}},
                    {{id: "1", name: "Нед. 1", field: "week1", resizable: true, width: 60, editor: Slick.Editors.Integer}},
                    {{id: "2", name: "Нед. 2", field: "week2", resizable: true, width: 60, editor: Slick.Editors.Integer}},
                    {{id: "3", name: "Нед. 3", field: "week3", resizable: true, width: 60, editor: Slick.Editors.Integer}},
                    {{id: "4", name: "Нед. 4", field: "week4", resizable: true, width: 60, editor: Slick.Editors.Integer}},
                    {{id: "5", name: "Нед. 5", field: "week5", resizable: true, width: 60, editor: Slick.Editors.Integer}},
                    {{id: "6", name: "Нед. 6", field: "week6", resizable: true, width: 60, editor: Slick.Editors.Integer}},
                    {{id: "7", name: "Нед. 7", field: "week7", resizable: true, width: 60, editor: Slick.Editors.Integer}},
                    {{id: "8", name: "Нед. 8", field: "week8", resizable: true, width: 60, editor: Slick.Editors.Integer}},
                    {{id: "9", name: "Нед. 9", field: "week9", resizable: true, width: 60, editor: Slick.Editors.Integer}},
                    {{id: "10", name: "Нед. 10", field: "week10", resizable: true, width: 60, editor: Slick.Editors.Integer}},
                    {{id: "11", name: "Нед. 11", field: "week11", resizable: true, width: 60, editor: Slick.Editors.Integer}},
                    {{id: "12", name: "Нед. 12", field: "week12", resizable: true, width: 60, editor: Slick.Editors.Integer}},
                    {{id: "13", name: "Нед. 13", field: "week13", resizable: true, width: 60, editor: Slick.Editors.Integer}},
                    {{id: "14", name: "Нед. 14", field: "week14", resizable: true, width: 60, editor: Slick.Editors.Integer}},
                    {{id: "15", name: "Нед. 15", field: "week15", resizable: true, width: 60, editor: Slick.Editors.Integer}},
                    {{id: "16", name: "Нед. 16", field: "week16", resizable: true, width: 60, editor: Slick.Editors.Integer}},
                    {{id: "17", name: "Нед. 17", field: "week17", resizable: true, width: 60, editor: Slick.Editors.Integer}},
                    {{id: "18", name: "Нед. 18", field: "week18", resizable: true, width: 60, editor: Slick.Editors.Integer}},
                    {{id: "19", name: "Нед. 19", field: "week19", resizable: true, width: 60, editor: Slick.Editors.Integer}},
                    {{id: "20", name: "Нед. 20", field: "week20", resizable: true, width: 60, editor: Slick.Editors.Integer}},


                  ];
                  var options = {{
                    editable: true,
                    autoHeight: true
                  }};

                grid = new Slick.Grid("#id_{name}_jsoneditor", data, columns, options);

                grid.onCellChange.subscribe(function (e, args) {{
                    console.log(JSON.stringify(grid.getData()));
                    $("#id_diagram").val(JSON.stringify(grid.getData()));
                }});
        }});
        </script>
        <div {attrs}></div>
        '''.format(
            attrs=flatatt(final_attrs),
            name=name,
            data=data
        )
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


@admin.register(WorkingType)
class WorkingTypeAdmin(VersionAdmin):
    list_display = ("title", "color")
