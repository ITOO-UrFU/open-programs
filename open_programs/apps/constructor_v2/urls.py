from django.conf.urls import url, include
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', index, name='constructor_index'),
    ]