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
    type_title = serializers.CharField(source='type.title', read_only=True)

    class Meta:
        model = Component
        fields = ("id", "title", "slug", "dev_description", "type_title", "weight", "content", "json")


class SubContainerSerializer(serializers.ModelSerializer):
    type_title = serializers.CharField(source='type.title', read_only=True)
    components = ComponentSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Container
        fields = ("id", "title", "slug", "dev_description", "type_title", "weight", "containers", "components")
        depth = 3


class ContainerSerializer(serializers.ModelSerializer):
    type_title = serializers.CharField(source='type.title', read_only=True)
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
        fields = ("id", "title", "slug", "dev_description", "type_title", "weight", "containers", "components")
        depth = 3



