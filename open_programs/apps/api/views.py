from courses.models import Course
from rest_framework import viewsets
from rest_framework import serializers
from courses.serializers import CourseSerializer


class CourseList(viewsets.ModelViewSet):
    """
    API endpoint that represents a list of users.
    """
    queryset = Course.objects.all().order_by('-created')
    serializer_class = CourseSerializer


class CourseDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course