from .models import Discipline, Variant, Diagram, Technology, Semester, TrainingTerms
from courses.models import Course
from programs.models import Program
from rest_framework import serializers
from courses.serializers import CourseSerializer


class DisciplineSerializer(serializers.HyperlinkedModelSerializer):

    results = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='result-detail'
    )

    class Meta:
        model = Discipline
        fields = ("title", "labor", "period", "results", "results_text", "status", "archived", "created", "updated")


class DiagramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagram
        fields = ("id", "title", "diagram")


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
    term = TrainingTermsSerializer()

    class Meta:
        model = Semester
        fields = ("discipline", "year", "admission_semester", "training_semester", "term")


class VariantSerializer(serializers.ModelSerializer):
    program = serializers.PrimaryKeyRelatedField(
        required=False,
        many=False,
        queryset=Program.objects.filter(status="p", archived=False)
    )
    discipline = serializers.PrimaryKeyRelatedField(
        required=False,
        many=False,
        queryset=Discipline.objects.filter(status="p", archived=False)
    )
    diagram = serializers.PrimaryKeyRelatedField(
        required=False,
        many=False,
        queryset=Diagram.objects.filter(status="p", archived=False)
    )
    technology = serializers.PrimaryKeyRelatedField(
        required=False,
        many=False,
        queryset=Technology.objects.filter(status="p", archived=False)
    )
    course = serializers.PrimaryKeyRelatedField(
        required=False,
        many=False,
        queryset=Course.objects.filter(status="p", archived=False)
    )

    class Meta:
        model = Variant
        fields = ("id", "program", "discipline", "diagram", "technology", "course", "semester", "parity", "link")
