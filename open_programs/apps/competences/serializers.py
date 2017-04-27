from .models import Competence
from results.serializers import ResultSerializer
from rest_framework import serializers


class CompetenceSerializer(serializers.HyperlinkedModelSerializer):
    results = ResultSerializer(many=True, read_only=True)
    class Meta:
        model = Competence
        fields = ("title", "results", "status", "archived", "created", "updated")
