from rest_framework import viewsets
from .serializers import *
from .models import Container, Component, ComponentType, ContainerType


class ContainerList(viewsets.ReadOnlyModelViewSet):
    queryset = Container.objects.filter(status="p", archived=False)
    serializer_class = ContainerSerializer


class ComponentList(viewsets.ReadOnlyModelViewSet):
    queryset = Component.objects.filter(status="p", archived=False)
    serializer_class = ComponentSerializer


class ComponentTypeList(viewsets.ReadOnlyModelViewSet):
    queryset = ComponentType.objects.all()
    serializer_class = ComponentTypeSerializer


class ContainerTypeList(viewsets.ReadOnlyModelViewSet):
    queryset = ContainerType.objects.all()
    serializer_class = ContainerTypeSerializer


class ContainerDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Container


class ComponentDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Component


class ComponentTypeDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ComponentType


class ContainerTypeDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ContainerType


class ContainerListByType(viewsets.ReadOnlyModelViewSet):
    serializer_class = ContainerSerializer
    lookup_field = 'get_type'
