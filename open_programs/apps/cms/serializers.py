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
    type = ComponentTypeSerializer(
        many=False,
        read_only=True
    )

    class Meta:
        model = Component
        fields = ("id", "title", "slug", "dev_description", "type", "weight", "content", "json")


class SubContainerSerializer(serializers.HyperlinkedModelSerializer):
    type = ContainerTypeSerializer(
        many=False,
        read_only=True
    )

    components = ComponentSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Container
        fields = ("id", "title", "slug", "dev_description", "type", "weight", "containers", "components")
        depth = 3


class ContainerSerializer(serializers.ModelSerializer):
    type = ContainerTypeSerializer(
        many=False,
        read_only=True
    )

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
        fields = ("id", "title", "slug", "dev_description", "type", "weight", "containers", "components")
        depth = 3

