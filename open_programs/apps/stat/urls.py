from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index, name='stat_index'),
    url(r'^(?P<id>.*)/$', instance, name='instance'),
    ]