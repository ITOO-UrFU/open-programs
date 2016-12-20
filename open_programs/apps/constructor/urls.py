from django.conf.urls import url, include
from .views import index, programs, courses, professions, program_detail, module_detail, discipline_remove, discipline_add

urlpatterns = [
        url(r'^$', index, name='index'),
        url(r'^programs/$', programs, name='programs'),
        url(r'^courses/$', courses, name='courses'),
        url(r'^professions/$', professions, name='professions'),

        url(r'^programs/(?P<pk>[0-9A-Za-z-]+)/$', program_detail, name='program_detail'),
        url(r'^modules/(?P<pk>[0-9A-Za-z-]+)/$', module_detail, name='module_detail'),
        url(r'^modules/remove/(?P<mod_pk>[0-9A-Za-z-]+)/(?P<disc_pk>[0-9]+)/$', discipline_remove, name='discipline_remove'),
        url(r'^modules/add/(?P<mod_pk>[0-9A-Za-z-]+)/(?P<disc_pk>[0-9]+)/$', discipline_add, name='discipline_add'),
        ]