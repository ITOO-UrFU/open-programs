from .models import Profession
from rest_framework import serializers


class ProfessionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profession
        fields = ("title", "description", "status", "archived", "created", "updated")