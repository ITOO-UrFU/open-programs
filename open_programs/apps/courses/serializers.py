from .models import Course, Session
from rest_framework import serializers


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ("title", "slug", "description", "about", "cover", "video", "video_cover", "workload", "points", "duration", "sessions", "results", "results_text", "status", "archived")
