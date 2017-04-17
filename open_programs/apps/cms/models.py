from django.db import models
from base.models import ObjectBaseClass
from jsonfield import JSONField
from django.utils.translation import ugettext_lazy as _
import uuid
from tinymce.models import HTMLField


def container_as_dict(container):
    return {
        "id": container.id,
        "slug": container.slug,
        "title": container.title,
        "html": container.html,
        "pages": container.get_pages_dict(),
        "keywords": container.keywords,
        "type": container.type.title,
        "weight": container.weight,
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
    title = models.CharField(_("Название типа контейнера"), max_length=256, blank=False, default=random_container_key)
    slug = models.SlugField(_("Код"), null=True)
    dev_description = HTMLField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'тип контейнера'
        verbose_name_plural = 'типы контейнера'


class ComponentType(models.Model):
    title = models.CharField(_("Название типа компонента"), max_length=256, blank=False, default=random_component_key)
    slug = models.SlugField(_("Код"), null=True)
    dev_description = HTMLField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'тип компонента'
        verbose_name_plural = 'типы компонентов'


class Container(ObjectBaseClass):
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
        return [container_as_dict(container) for container in self.containers.filter(status="p").order_by('weight')]


class Component(ObjectBaseClass):
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

