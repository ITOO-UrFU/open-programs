from django.contrib import admin

from jsoneditor.fields.django_jsonfield import JSONField
from jsoneditor.forms import JSONEditor
from reversion.admin import VersionAdmin
from codemirror2.widgets import CodeMirrorEditor

from .models import Component, ComponentType
from .models import Container, ContainerType


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
