from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^$', index, name='constructor_index'),
    url(r'^programs/$', programs, name='programs'),
    url(r'^courses/$', courses, name='courses'),
    url(r'^professions/$', professions, name='professions'),

    url(r'^courses/create/$', course_create, name='course_create'),
    url(r'^professions/create/$', profession_create, name='profession_create'),

    url(r'^programs/(?P<pk>[0-9A-Za-z-]+)/$', program_detail, name='program_detail'),
    url(r'^programs/add/(?P<program_pk>[0-9A-Za-z-]+)/(?P<module_pk>[0-9A-Za-z-]+)/$', program_add, name='program_add'),
    url(r'^programs/remove/(?P<program_pk>[0-9A-Za-z-]+)/(?P<module_pk>[0-9A-Za-z-]+)/$', program_remove, name='program_remove'),
    url(r'^modules/(?P<pk>[0-9A-Za-z-]+)/$', module_detail, name='module_detail'),
    url(r'^modules/remove/(?P<mod_pk>[0-9A-Za-z-]+)/(?P<disc_pk>[0-9]+)/$', discipline_remove, name='discipline_remove'),
    url(r'^modules/add/(?P<mod_pk>[0-9A-Za-z-]+)/(?P<disc_pk>[0-9]+)/$', discipline_add, name='discipline_add'),
    url(r'^disciplines/(?P<pk>[0-9]+)/$', discipline_detail, name='discipline_detail'),
    url(r'^disciplines/remove/(?P<disc_pk>[0-9A-Za-z-]+)/(?P<course_pk>[0-9]+)/$', course_remove, name='course_remove'),
    url(r'^disciplines/add/(?P<disc_pk>[0-9A-Za-z-]+)/(?P<course_pk>[0-9]+)/$', course_add, name='course_add'),
    url(r'^professions/(?P<pk>[0-9A-Za-z-]+)/$', profession_detail, name='profession_detail'),
    #url(r'^professions/edit/(?P<pk>[0-9A-Za-z-]+)/$', professions_edit, name='professions_edit'),
    url(r'^courses/(?P<pk>[0-9A-Za-z-]+)/$', course_detail, name='course_detail'),
    url(r'^courses/remove/(?P<course_pk>[0-9A-Za-z-]+)/(?P<result_pk>[0-9]+)/$', result_remove, name='result_remove'),
    url(r'^courses/add/(?P<course_pk>[0-9A-Za-z-]+)/(?P<result_pk>[0-9]+)/$', course_add_result, name='course_add_result'),
    url(r'^result/create/(?P<course_pk>[0-9A-Za-z-]+)$', result_create, name='result_create'),
    url(r'^result/create/(?P<comp_pk>[0-9A-Za-z-]+)/(?P<prof_pk>[0-9A-Za-z-]+)$', competence_result_create, name='competence_result_create'),
    url(r'^result/create/(?P<comp_pk>[0-9A-Za-z-]+)/$', competence_result_create_noprof,
        name='competence_result_create_noprof'),

    url(r'^competence/edit/(?P<pk>[0-9A-Za-z-]+)/$', competence_edit, name='competence_edit'),
    url(r'^competence/create/(?P<pk>[0-9]+)$', competence_create, name='competence_create'),
    url(r'^module/create/$', module_create, name='module_create'),
    url(r'^discipline/create/(?P<module_pk>[0-9A-Za-z-]+)$', discipline_create, name='discipline_create'),
    url(r'^profession/remove/(?P<prof_pk>[0-9A-Za-z-]+)/(?P<comp_pk>[0-9]+)/$', competence_profession_remove, name='competence_profession_remove'),
    url(r'^profession/add/(?P<prof_pk>[0-9A-Za-z-]+)/(?P<comp_pk>[0-9]+)/$', competence_profession_add, name='competence_profession_add'),
    url(r'^competence/add/(?P<comp_pk>[0-9A-Za-z-]+)/(?P<result_pk>[0-9]+)/$', competence_result_add, name='competence_result_add'),
    url(r'^competence/remove/(?P<comp_pk>[0-9A-Za-z-]+)/(?P<result_pk>[0-9]+)/$', competence_result_remove, name='competence_result_remove'),

    ]