from .models import Course, Session
from rest_framework import serializers


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    # authors = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='person-detail'
    # )
    #
    # staff = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='person-detail'
    # )

    sessions = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='session-detail'
    )

    results = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='result-detail'
    )

    class Meta:
        model = Course
        fields = ("id", "title", "description", "slug", "about", "cover", "video", "video_cover", "workload", "points",
                  "duration", "sessions",  "results", "results_text", "status", "archived", "created",
                  "updated")  # "authors", "authors_ordering", "staff",


class CourseIdSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Course
        fields = ('id',)
        read_only_fields = ('id',)


class SessionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Session
        fields = ("slug", "startdate", "enddate", "status", "archived", "created", "updated")
