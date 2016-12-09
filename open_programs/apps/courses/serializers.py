from .models import Course, Session
from rest_framework import serializers


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ("title", "slug", "description", "about")
