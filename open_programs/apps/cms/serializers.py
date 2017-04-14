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


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ("id", "title", "slug", "dev_description", "get_type", "weight", "content", "json")


class SubContainerSerializer(serializers.ModelSerializer):
    components = ComponentSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Container
        fields = ("id", "title", "slug", "dev_description", "get_type", "weight", "containers", "components")
        depth = 3


class ContainerSerializer(serializers.ModelSerializer):

    containers = SubContainerSerializer(
        many=True,
        read_only=True
    )

    components = ComponentSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Container
        fields = ("id", "title", "slug", "dev_description", "get_type", "weight", "containers", "components")
        depth = 3



