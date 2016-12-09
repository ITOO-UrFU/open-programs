from .models import Person
from django.contrib.auth.models import User
from rest_framework import serializers


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = ("user", "first_name", "last_name", "second_name", "sex", "alt_email", "birthday_date", "biography")  # "country" is not JSON serializable


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")