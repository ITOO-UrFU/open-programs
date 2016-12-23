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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from django.views.generic.base import RedirectView

from dashing.utils import router
import permission

from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_swagger.views import get_swagger_view

from api.views import *

permission.autodiscover()


router = routers.DefaultRouter()
router.register(r'courses', CourseList)
router.register(r'courses_ids', CoursesIdList, 'Course')
router.register(r'sessions', SessionList)
router.register(r'persons', PersonList)
router.register(r'users', UserList)
router.register(r'competences', CompetenceList)
router.register(r'results', ResultList)
router.register(r'programs', ProgramList)
router.register(r'disciplines', DisciplineList)

router.register(r'modules', ModuleList)
router.register(r'types', TypeList)
router.register(r'generalbasemodulespools', GeneralBaseModulesPoolList)
router.register(r'educationalprogramtrajectoriespools', EducationalProgramTrajectoriesPoolList)
router.register(r'choicemodulespools', ChoiceModulesPoolList)



schema_view = get_swagger_view(title='Open programs')


urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/constructor/', permanent=False), name='index'),

    url(r'^admin/', include('smuggler.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/', include(router.urls, namespace='api')),
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
    url(r'constructor/', include('constructor.urls')),
]