from .models import Result
from rest_framework import serializers


class ResultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Result
        fields = ("id", "title", "status", "archived", "created", "updated")