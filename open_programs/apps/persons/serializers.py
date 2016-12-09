from .models import Person
from rest_framework import serializers


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = ("user", "first_name", "last_name", "second_name", "sex", "alt_email", "country", "birthday_date", "biography", "status", "archived", "created", "updated")