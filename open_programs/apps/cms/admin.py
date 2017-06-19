from django.contrib import admin

from jsonfield import JSONField
from reversion.admin import VersionAdmin

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
        final_attrs = self.build_attrs(div_attrs=div_attrs, extra_attrs={"name": name})
        r += '''
        <style type="text/css">
            #id_%(name)s_jsoneditor {
              height: 400px;
              margin-bottom: 1em;
            }
          </style>
        <script>

        document.addEventListener("DOMContentLoaded", function(event) {
            var jsoncontainer = document.getElementById("id_%(name)s_jsoneditor");
            var options = {
                mode: 'code',
                modes: ['code', 'tree'],
                onChange: function(){document.getElementById("id_%(name)s").value = JSON.stringify(editor.get())}
            };
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


@admin.register(Component)
class ComponentAdmin(VersionAdmin):

    formfield_overrides = {
        JSONField: {'widget': JSONEditor},
    }

    fields = ("title", "slug", "type", "weight", "status", "archived", "content", "json", "dev_description")
    list_display = ("title", "slug", "weight", "status", "archived")
    list_filter = ("slug", "weight", "status", "archived")
    search_fields = ('slug', "title", "dev_description")


@admin.register(Container)
class ContainerAdmin(VersionAdmin):
    fields = ("title", "slug", "type", "weight", "status", "archived", "containers", "components", "dev_description")
    list_display = ("title", "slug", "weight", "status", "archived")
    filter_horizontal = ("containers", "components")
    list_filter = ("slug", "weight", "status", "archived")
    search_fields = ('slug', "title", "dev_description")


@admin.register(ContainerType)
class ContainerTypeAdmin(VersionAdmin):
    fields = ("title", "slug", "dev_description")


@admin.register(ComponentType)
class ComponentTypeAdmin(VersionAdmin):
    fields = ("title", "slug", "dev_description")
