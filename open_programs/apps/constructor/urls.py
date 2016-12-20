from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^$', index, name='constructor_index'),
    url(r'^programs/$', programs, name='programs'),
    url(r'^courses/$', courses, name='courses'),
    url(r'^professions/$', professions, name='professions'),

    url(r'^programs/(?P<pk>[0-9A-Za-z-]+)/$', program_detail, name='program_detail'),
    url(r'^programs/add/(?P<program_pk>[0-9A-Za-z-]+)/(?P<module_pk>[0-9A-Za-z-]+)/$', program_add, name='program_add'),
    url(r'^programs/remove/(?P<program_pk>[0-9A-Za-z-]+)/(?P<module_pk>[0-9A-Za-z-]+)/$', program_remove, name='program_remove'),
    url(r'^modules/(?P<pk>[0-9A-Za-z-]+)/$', module_detail, name='module_detail'),
    url(r'^modules/remove/(?P<mod_pk>[0-9A-Za-z-]+)/(?P<disc_pk>[0-9]+)/$', discipline_remove, name='discipline_remove'),
    url(r'^modules/add/(?P<mod_pk>[0-9A-Za-z-]+)/(?P<disc_pk>[0-9]+)/$', discipline_add, name='discipline_add'),
    url(r'^disciplines/(?P<pk>[0-9]+)/$', discipline_detail, name='discipline_detail'),
    url(r'^disciplines/remove/(?P<disc_pk>[0-9A-Za-z-]+)/(?P<course_pk>[0-9]+)/$', course_remove, name='course_remove'),
    url(r'^disciplines/add/(?P<disc_pk>[0-9A-Za-z-]+)/(?P<course_pk>[0-9]+)/$', course_add, name='course_add'),
    ]
