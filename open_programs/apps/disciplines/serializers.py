from .models import Discipline, Variant, Diagram, Technology, Semester, TrainingTerms
from courses.models import Course
from rest_framework import serializers
from courses.serializers import CourseSerializer
from programs.serializers import ProgramSerializer


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


class TrainingTermsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingTerms
        fields = ("title", "limit")


class SemesterSerializer(serializers.ModelSerializer):
    discipline = DisciplineSerializer()
    program = ProgramSerializer()
    term = TrainingTermsSerializer()

    class Meta:
        model = Semester
        fields = ("discipline", "program", "year", "admission_semester", "training_semester", "term")


class VariantSerializer(serializers.ModelSerializer):
    program = ProgramSerializer()
    discipline = DisciplineSerializer()
    diagram = DiagramSerializer()
    technology = TechnologySerializer()
    course = CourseSerializer()

    class Meta:
        model = Variant
        fields = ("program", "discipline", "diagram", "technology", "course", "semester", "parity", "link")
