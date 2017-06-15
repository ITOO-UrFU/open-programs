"""open_programs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import permission
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework import routers

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

from rest_framework_swagger.views import get_swagger_view

from ajax_select import urls as ajax_select_urls

from .apps.api.views import *
from .apps.api_v11.views import *

permission.autodiscover()


router_10 = routers.DefaultRouter()
router_10.register(r'courses', CourseList)
router_10.register(r'courses_ids', CoursesIdList, 'Course')
router_10.register(r'sessions', SessionList)
router_10.register(r'persons', PersonList)
router_10.register(r'users', UserList)
router_10.register(r'competences', CompetenceList)
router_10.register(r'results', ResultList)
router_10.register(r'programs', ProgramList)
router_10.register(r'disciplines', DisciplineList)
router_10.register(r'modules', ModuleList)
router_10.register(r'types', TypeList)

router_11 = routers.DefaultRouter()
router_11.register(r'choice_group_types', ChoiceGroupTypeList)
router_11.register(r'choice_groups', ChoiceGroupList)
router_11.register(r'target_modules', TargetModulesList)
router_11.register(r'program_modules', ProgramModulesList)
router_11.register(r'program_competences', ProgramCompetenceList)
router_11.register(r'training_targets', TrainingTargetList)
router_11.register(r'users', UserList)
router_11.register(r'courses', CourseList)
router_11.register(r'persons', PersonList)
router_11.register(r'competences', CompetenceList)
router_11.register(r'results', ResultList)
router_11.register(r'disciplines', DisciplineList)
router_11.register(r'types', TypeList)
router_11.register(r'modules', ModuleList)
router_11.register(r'programs', ProgramList)
router_11.register(r'components', ComponentList)
router_11.register(r'componenttypes', ComponentTypeList)
router_11.register(r'diagrams', DiagramList)
router_11.register(r'technologies', TechnologyList)
router_11.register(r'training_terms', TrainingTermsList)
router_11.register(r'semesters', SemesterList)
router_11.register(r'variants', VariantList)


schema_view = get_swagger_view(title='Open programs')


urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/constructor/', permanent=False), name='index'),

    url(r'^admin/', include('smuggler.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^ajax_select/', include(ajax_select_urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/', include(router_10.urls, namespace='api')),
    url(r'^api/v11/', include(router_11.urls, namespace='api_v11')),
    url(r'^api/docs/', schema_view),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^api/v11/api-token-auth/', obtain_jwt_token),
    url(r'^api/v11/api-token-refresh/', refresh_jwt_token),
    url(r'^api/v11/api-token-verify/', verify_jwt_token),
 ]


if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [url(r'^rosetta/', include('rosetta.urls')),
                    url(r'^i18n/', include('django.conf.urls.i18n')),
                    ]

if settings.DEBUG is True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#### APPS ####

urlpatterns += [
    url(r'^constructor/', include('open_programs.apps.constructor.urls')),
    url(r'^constructor_v2/', include('open_programs.apps.constructor_v2.urls')),
]

#### API rewrite
urlpatterns.append(url(r'^api/v11/heartbeat/$', heartbeat, name="heartbeat"))
urlpatterns.append(url(r'^api/v11/get_program_choice_groups/(?P<program_id>.*)/$', get_choice_groups_by_program, name="get_choice_groups_by_program"))
urlpatterns.append(url(r'^api/v11/get_program_modules/(?P<program_id>.*)/$', get_program_modules, name="get_program_modules"))
urlpatterns.append(url(r'^api/v11/get_program_targets/(?P<program_id>.*)/$', get_targets_by_program, name="get_targets_by_program"))
urlpatterns.append(url(r'^api/v11/get_program_competences/(?P<program_id>.*)/$', get_competences_by_program, name="get_competences_by_program"))
urlpatterns.append(url(r'^api/v11/change_target_module/$', change_target_module, name="change_target_module"))
urlpatterns.append(url(r'^api/v11/change_choice_group/$', change_choice_group, name="change_choice_group"))
urlpatterns.append(url(r'^api/v11/change_competence/$', change_competence, name="change_competence"))

urlpatterns.append(url(r'^api/v11/get_program_disciplines/(?P<program_id>.*)/$', get_program_disciplines, name="get_program_disciplines"))
urlpatterns.append(url(r'^api/v11/change_discipline_semester/$', change_discipline_semester, name="change_discipline_semester"))
urlpatterns.append(url(r'^api/v11/get_variants/(?P<program_id>.*)/(?P<discipline_id>.*)/$', get_variants, name="get_variants"))
urlpatterns.append(url(r'^api/v11/change_variant/$', change_variant, name="change_variant"))
urlpatterns.append(url(r'^api/v11/delete_variant/$', delete_variant, name="delete_variant"))
urlpatterns.append(url(r'^api/v11/create_variant/$', create_variant, name="create_variant"))

urlpatterns.append(url(r'^api/v11/new_trajectory/$', new_trajectory, name="new_trajectory"))
urlpatterns.append(url(r'^api/v11/save_trajectory/$', save_trajectory, name="save_trajectory"))

urlpatterns.append(url(r'^api/v11/get_program_variants/(?P<program_id>.*)/$', get_program_variants, name="get_program_variants"))
#### CMS API ####
urlpatterns.append(url(r'^api/v11/containers/$', get_containers, name="get_containers"))
urlpatterns.append(url(r'^api/v11/containers_by_type/(?P<slug>.*)/$', containers_by_type, name="containers_by_type"))
urlpatterns.append(url(r'^api/v11/container_by_slug/(?P<slug>.*)/$', container_by_slug, name="container_by_slug"))
