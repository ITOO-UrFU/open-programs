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
from rest_framework_swagger.views import get_swagger_view

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


schema_view = get_swagger_view(title='Open programs')


urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/constructor/', permanent=False), name='index'),

    url(r'^admin/', include('smuggler.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/', include(router_10.urls, namespace='api')),
    url(r'^api/v11/', include(router_11.urls, namespace='api_v11')),
    url(r'^api/docs/', schema_view),
 ]


if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [url(r'^rosetta/', include('rosetta.urls')),
                    url(r'^i18n/', include('django.conf.urls.i18n')),
                    url(r'^accounts/', include('allauth.urls')),
                    ]

if settings.DEBUG is True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#### APPS ####

urlpatterns += [
    url(r'constructor/', include('open_programs.apps.constructor.urls')),
    url(r'constructor_v2/', include('open_programs.apps.constructor_v2.urls')),
]

#### API rewrite
urlpatterns.append(url(r'^api/v11/get_choice_groups_by_program/(?P<program_id>.*)/$', get_choice_groups_by_program, name="get_choice_groups_by_program"))
urlpatterns.append(url(r'^api/v11/get_program_modules/(?P<program_id>.*)/$', get_program_modules, name="get_program_modules"))