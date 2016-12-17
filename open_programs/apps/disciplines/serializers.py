from .models import Discipline
from courses.models import Course
from rest_framework import serializers
from courses.serializers import CourseSerializer


class DisciplineSerializer(serializers.HyperlinkedModelSerializer):
    courses = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )

    results = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='result-detail'
    )

    class Meta:
        model = Discipline
        fields = ("name", "courses", "results", "results_text", "status", "archived", "created", "updated")