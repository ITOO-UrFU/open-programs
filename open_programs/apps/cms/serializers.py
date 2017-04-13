from .models import ContainerType, ComponentType, Container
from rest_framework import serializers


class ContainerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContainerType
        fields = ("slug",)


class ComponentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentType
        fields = ("slug",)


class ContainerSerializer(serializers.ModelSerializer):
    type = ContainerTypeSerializer(
        many=False,
    )

    class Meta:
        model = Container
        fields = ("id", "title", "slug", "dev_description", "type", "weight", "containers")  # TODO: add components


class ComponentSerializer(serializers.ModelSerializer):
    type = ComponentTypeSerializer(
        many=False,
    )

    class Meta:
        model = Container
        fields = ("id", "title", "slug", "dev_description", "type", "weight", "containers", "content", "json")  # TODO: add components
