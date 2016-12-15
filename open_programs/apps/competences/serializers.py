from .models import Competence
from rest_framework import serializers


class CompetenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Competence
        fields = ("title", "results", "status", "archived", "created", "updated")
