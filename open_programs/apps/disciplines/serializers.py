from .models import Discipline, Variant, Diagram, Technology, Semester, TrainingTerms
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
        fields = ("title", "courses", "labor", "period", "results", "results_text", "status", "archived", "created", "updated")


class DiagramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagram
        fields = ("title", "diagram")


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = ("title", "description", "contact_work_category", "color")


class SemesterSerializer(serializers.ModelSerializer):
    discipline = DisciplineSerializer()
    term = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=True
    )

    class Meta:
        model = Semester
        fields = ("discipline", "year", "admission_semester", "training_semester", "term")


class VariantSerializer(serializers.ModelSerializer):
    discipline = DisciplineSerializer()
    diagram = DiagramSerializer()
    technology = TechnologySerializer()
    course = CourseSerializer()

    class Meta:
        model = Variant
        fields = ("discipline", "diagram", "technology", "course", "semester", "parity", "link")
