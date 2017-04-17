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


class ComponentDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Component


class ComponentTypeDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ComponentType


@api_view(('GET',))
def get_containers(request):
    queryset = Container.objects.filter(status="p", archived=False)
    context = [
        {
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
def containers_by_type(request, slug):
    queryset = Container.objects.filter(status="p", archived=False, type__slug=slug)
    context = [
        {
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
def container_by_slug(request, slug):
    """
        Returns a list of all **active** accounts in the system.

        For more details on how accounts are activated please [see here][ref].

        [ref]: http://example.com/activating-accounts
    """
    queryset = Container.objects.filter(status="p", archived=False, slug=slug)
    context = [
        {
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
