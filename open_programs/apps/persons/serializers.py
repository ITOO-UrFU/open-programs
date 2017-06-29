from .models import Person
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "is_staff", "groups")

    def validate(self, data):
        if not data['username'] and not data['email']:
            raise serializers.ValidationError("Not enought data")
        return data


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(
        many=False,
        read_only=False,
    )

    class Meta:
        model = Person
        fields = ("user", "first_name", "last_name", "second_name", "sex", "alt_email", "birthday_date", "biography")  # "country" is not JSON serializable

