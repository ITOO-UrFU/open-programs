from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import Container, Component, ComponentType, ContainerType


class ComponentList(viewsets.ReadOnlyModelViewSet):
    queryset = Component.objects.filter(status="p", archived=False)
    serializer_class = ComponentSerializer


class ComponentTypeList(viewsets.ReadOnlyModelViewSet):
    queryset = ComponentType.objects.all()
    serializer_class = ComponentTypeSerializer


class ContainerTypeList(viewsets.ReadOnlyModelViewSet):
    queryset = ContainerType.objects.all()
    serializer_class = ContainerTypeSerializer


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
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer
    lookup_field = 'get_type'


@api_view(('GET',))
def get_containers(request):
    queryset = Container.objects.filter(status="p", archived=False)
    context = [
        {
            "id": c.id,
            "title": c.title,
            "slug": c.slug,
            "type": c.type.slug,
            "weight": c.weight,
            "containers": c.get_containers_dict(),
            "components": c.get_components_dict()
        }
        for c in queryset
        ]

    return Response(context)


@api_view(('GET',))
def get_containers_by_slug(request, slug):
    queryset = Container.objects.filter(status="p", archived=False, type__slug=slug)
    context = [
        {
            "id": c.id,
            "title": c.title,
            "slug": c.slug,
            "type": c.type.slug,
            "weight": c.weight,
            "containers": c.get_containers_dict(),
            "components": c.get_components_dict()
        }
        for c in queryset
        ]

    return Response(context)