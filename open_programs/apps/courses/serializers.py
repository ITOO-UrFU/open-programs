from .models import Course, Session
from rest_framework import serializers


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "title", "description",  "slug", "authors", "authors_ordering", "about", "cover", "video", "video_cover", "workload", "points", "duration", "sessions", "staff", "results", "results_text", "status", "archived", "created", "updated")


class SessionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Session
        fields = ("slug", "startdate", "enddate", "status", "archived", "created", "updated")
