from django.contrib import admin

from jsonfield import JSONField
from jsoneditor.forms import JSONEditor



class MyAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField:{'widget': JSONEditor},
    }
