from .models import ContainerType, ComponentType, Container, Component
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
        fields = ("id", "title", "slug", "dev_description", "type", "weight", "containers", "components")
        read_only_fields = fields


class ComponentSerializer(serializers.ModelSerializer):
    type = ComponentTypeSerializer(
        many=False,
    )

    class Meta:
        model = Component
        fields = ("id", "title", "slug", "dev_description", "type", "weight", "content", "json")
        read_only_fields = fields
