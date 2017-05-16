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
            input_attrs['class'] = 'for_jsoneditor'
        else:
            input_attrs['class'] += ' for_jsoneditor'
        r = super(JSONEditor, self).render(name, value, input_attrs)
        div_attrs = {}
        div_attrs.update(attrs)
        div_attrs.update({'id': (attrs['id']+'_jsoneditor')})
        final_attrs = self.build_attrs(div_attrs, extra_attrs={"name": name})
        r += '''
        <style type="text/css">
            #id_%(name)s_jsoneditor {
              height: 400px;
              margin-bottom: 1em;
            }
          </style>
        <script>

        document.addEventListener("DOMContentLoaded", function(event) {
            var grid = document.getElementById("id_%(name)s_jsoneditor");

            var editor = new JSONEditor(jsoncontainer, options);

            editor.set(JSON.parse(document.getElementById("id_%(name)s").value.replace(/'/g, '"')));
            document.getElementById("id_%(name)s").value = JSON.stringify(editor.get());
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
