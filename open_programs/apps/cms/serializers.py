from .models import Type, Module
from rest_framework import serializers


class ContainerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ("slug",)


class ComponentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ("slug",)


class ContainerSerializer(serializers.dModelSerializer):
    type = ContainerTypeSerializer(
        many=True,
    )

    class Meta:
        model = Module
        fields = ("id", "title", "slug", "dev_description", "type", "weight", "containers")  # TODO: add components
