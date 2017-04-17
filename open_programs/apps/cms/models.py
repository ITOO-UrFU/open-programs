from django.db import models
from base.models import ObjectBaseClass
from jsonfield import JSONField
from django.utils.translation import ugettext_lazy as _
import uuid
from tinymce.models import HTMLField


def container_as_dict(c):
    return {
        "id": c.id,
        "title": c.title,
        "slug": c.slug,
        "type": c.type.slug,
        "weight": c.weight,
        "containers": c.get_containers_dict(),
        "components": c.get_components_dict()
    }


def component_as_dict(c):
    return {
        "id": c.id,
        "title": c.title,
        "slug": c.slug,
        "type": c.type.slug,
        "weight": c.weight,
        "content": c.content,
        "json": c.json
    }


def random_container_key():
    key = uuid.uuid4().hex[:5]
    title = _("C")
    return "{title}_{key}".format(key=key, title=title)


def random_component_key():
    key = uuid.uuid4().hex[:5]
    title = _("C")
    return "{title}_{key}".format(key=key, title=title)


class ContainerType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("Название типа контейнера"), max_length=256, blank=False, default=random_container_key)
    slug = models.SlugField(_("Код"), null=True)
    dev_description = HTMLField(blank=True, null=True)

    def __str__(self):
        return "{} - {}".format(self.slug, self.title)

    class Meta:
        verbose_name = 'тип контейнера'
        verbose_name_plural = 'типы контейнера'


class ComponentType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("Название типа компонента"), max_length=256, blank=False, default=random_component_key)
    slug = models.SlugField(_("Код"), null=True)
    dev_description = HTMLField(blank=True, null=True)

    def __str__(self):
        return "{} - {}".format(self.slug, self.title)

    class Meta:
        verbose_name = 'тип компонента'
        verbose_name_plural = 'типы компонентов'


class Container(ObjectBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("Название контейнера"), max_length=256, blank=False, default=random_container_key)
    slug = models.SlugField(_("Код"))
    dev_description = HTMLField(blank=True, null=True)
    type = models.ForeignKey("ContainerType", blank=True, null=True)
    weight = models.IntegerField(_("Вес"), default=0)
    containers = models.ManyToManyField("self", verbose_name=_("Вложенные контейнеры"), blank=True, related_name='+', symmetrical=False)
    components = models.ManyToManyField("Component", verbose_name=_("Вложенные компоненты"), blank=True)

    class Meta:
        verbose_name = 'контейнер'
        verbose_name_plural = 'контейнеры'

    def __str__(self):
        return self.title

    def get_containers_dict(self):
        return [container_as_dict(container) for container in self.containers.filter(status="p", archived=False).order_by('weight')]

    def get_components_dict(self):
        return [component_as_dict(component) for component in self.components.filter(status="p", archived=False).order_by('weight')]


class Component(ObjectBaseClass):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("Название компонента"), max_length=256, blank=False, default=random_component_key)
    slug = models.SlugField(_("Код"))
    dev_description = HTMLField(verbose_name=_("DEV_DESCRIPTION"), blank=True, null=True)
    type = models.ForeignKey("ComponentType", blank=True, null=True)
    weight = models.IntegerField(_("Вес"), default=0)
    content = HTMLField(_("Контент"), blank=True, null=True)
    json = JSONField(verbose_name=_("JSON"), null=True, blank=True)

    class Meta:
        verbose_name = 'компонент'
        verbose_name_plural = 'компонент'

    def __str__(self):
        return self.title


