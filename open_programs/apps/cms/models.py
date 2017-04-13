from django.db import models
from base.models import ObjectBaseClass
from jsonfield import JSONField
from django.utils.translation import ugettext_lazy as _
import uuid
from tinymce.models import HTMLField


def random_container_key():
    key = uuid.uuid4().hex[:5]
    title = _("Контейнер")
    return "{title} {key}".format(key=key, title=title)


def random_component_key():
    key = uuid.uuid4().hex[:5]
    title = _("Контейнер")
    return "{title} {key}".format(key=key, title=title)


class ContainerType(models.Model):
    title = models.CharField(_("Название типа контейнера"), max_length=256, blank=False, default=random_container_key)
    dev_description = HTMLField()

    def __str__(self):
        return self.title


class ComponentType(models.Model):
    title = models.CharField(_("Название типа компонента"), max_length=256, blank=False, default=random_component_key)
    dev_description = HTMLField()

    def __str__(self):
        return self.title


class Container(ObjectBaseClass):
    title = models.CharField(_("Название контейнера"), max_length=256, blank=False, default=random_container_key)
    slug = models.SlugField(_("Код"))
    dev_description = HTMLField(blank=True, null=True)
    type = models.ForeignKey("ContainerType", blank=True, null=True)
    weight = models.IntegerField(_("Вес"), default=0)
    containers = models.ManyToManyField("self", verbose_name=_("Вложенные контейнеры"), blank=True, related_name='+', symmetrical=False)

    class Meta:
        verbose_name = 'контейнер'
        verbose_name_plural = 'контейнеры'

    def __str__(self):
        return self.title


class Component(ObjectBaseClass):
    title = models.CharField(_("Название компонента"), max_length=256, blank=False, default=random_component_key)
    slug = models.SlugField(_("Код"))
    dev_description = HTMLField(verbose_name=_("Описание"), blank=True, null=True)
    type = models.ForeignKey("ComponentType", blank=True, null=True)
    weight = models.IntegerField(_("Вес"), default=0)
    content = HTMLField(_("Контент"), blank=True, null=True)
    json = JSONField(verbose_name=_("JSON"), null=True, blank=True)
    components = models.ManyToManyField("self", verbose_name=_("Вложенные компоненты"), blank=True, related_name='+', symmetrical=False)

    class Meta:
        verbose_name = 'компонент'
        verbose_name_plural = 'компонент'

    def __str__(self):
        return self.title
