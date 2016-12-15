from .models import Result
from rest_framework import serializers


class ResultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Result
        fields = ("title", "status", "archived", "created", "updated")