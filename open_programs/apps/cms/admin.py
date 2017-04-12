from django.contrib import admin

from jsonfield import JSONField
from reversion.admin import VersionAdmin
from codemirror2.widgets import CodeMirrorEditor

from .models import Component, ComponentType
from .models import Container, ContainerType

from django.forms.widgets import Textarea
try:
    from django.forms.util import flatatt
except ImportError:
    from django.forms.utils import flatatt
from django.utils.safestring import mark_safe
from django.conf import settings
import json


class JSONEditor(Textarea):
    class Media:
        js = (
            getattr(settings, "JSON_EDITOR_JS", settings.STATIC_URL+'jsoneditor/jsoneditor.js'),
        )
        css = {'all': (getattr(settings, "JSON_EDITOR_CSS", settings.STATIC_URL+'jsoneditor/jsoneditor.css'),)}

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
        final_attrs = self.build_attrs(div_attrs, name=name)
        r += '''
        <style type="text/css">
            #id_json_jsoneditor {
              height: 700px;
            }
          </style>
        <script>

        document.addEventListener("DOMContentLoaded", function(event) {
            var jsoncontainer = document.getElementById("id_json_jsoneditor");
            var options = {
                onChange: function(){document.getElementById("id_json").value = editor.get()}
            };
            var editor = new JSONEditor(jsoncontainer, options);
        });

        </script>
        <div %(attrs)s></div>
        ''' % {
            'attrs': flatatt(final_attrs),
        }
        return mark_safe(r)


@admin.register(Component)
class ComponentAdmin(VersionAdmin):

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.attname in ("description", "about"):
            kwargs['widget'] = CodeMirrorEditor(options={'mode': 'htmlmixed', 'lineNumbers': True, 'lineWrapping': True},
                                                modes=['css', 'xml', 'javascript', 'htmlmixed'],
                                                )
        return super(ComponentAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    formfield_overrides = {
        JSONField: {'widget': JSONEditor},
    }

    fields = ("title", "slug", "type",  "dev_description", "content", "json", "components", "weight", "status", "archived")
    list_display = ("title", "slug", "weight", "status", "archived")
    filter_horizontal = ("components", )
    list_filter = ("slug", "weight", "status", "archived")
    search_fields = ('slug', "title", "dev_description")
