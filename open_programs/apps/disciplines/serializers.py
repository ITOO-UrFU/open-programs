from .models import Discipline
from rest_framework import serializers


class DisciplineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Discipline
        fields = ("name", "courses", "results", "results_text", "status", "archived", "created", "updated")