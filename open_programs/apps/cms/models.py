from django.db import models
from base.models import ObjectBaseClass
from django.utils.translation import ugettext_lazy as _
import uuid


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
    dev_description = models.TextField(_("Описание"), max_length=16384, blank=True, default="")  # TODO: WYSIWYG

    def __str__(self):
        return self.title


class ComponentType(models.Model):
    title = models.CharField(_("Название типа компонента"), max_length=256, blank=False, default=random_component_key)
    dev_description = models.TextField(_("Описание"), max_length=16384, blank=True, default="")  # TODO: WYSIWYG

    def __str__(self):
        return self.title


class Container(ObjectBaseClass):
    title = models.CharField(_("Название контейнера"), max_length=256, blank=False, default=random_container_key)
    slug = models.SlugField(_("Код"))
    dev_description = models.TextField(_("Описание"), max_length=16384, blank=True, default="")  # TODO: WYSIWYG
    #  TODO: Container m2m, type, component m2m, weight

    class Meta:
        verbose_name = 'контейнер'
        verbose_name_plural = 'контейнеры'

    def __str__(self):
        return self.title


class Component(ObjectBaseClass):
    title = models.CharField(_("Название компонента"), max_length=256, blank=False, default=random_component_key)
    slug = models.SlugField(_("Код"))
    dev_description = models.TextField(_("Описание"), max_length=16384, blank=True, default="")  # TODO: WYSIWYG
    # TODO: TYPE, content, json, weight

    class Meta:
        verbose_name = 'компонент'
        verbose_name_plural = 'компонент'

    def __str__(self):
        return self.title
