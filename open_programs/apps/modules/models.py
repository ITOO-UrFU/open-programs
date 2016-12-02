from django.utils.translation import ugettext_lazy as _

from django.db import models
import uuid


class Module(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("Название модуля"), max_length=256, blank=False, default=_("Название модуля"))
    description = models.TextField(_("Описание модуля"), max_length=16384, blank=True, default="")
    # TODO: M2M Discipline

    class Meta:
        verbose_name = 'модуль'
        verbose_name_plural = 'модули'

    def __str__(self):
        return self.title


class ModulesPool(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("Название пула модулей для траектории образовательной программы"), max_length=256, blank=False, default=_("Название пула"))
    description = models.TextField(_("Описание"), max_length=16384, blank=True, default="")
    modules = models.ManyToManyField(Module)

    class Meta:
        verbose_name = 'пул модулей'
        verbose_name_plural = 'пулы модулей'

    def get_all(self):
        return "\n".join([str(module)for module in self.modules.all()])


class ChoicePool(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("Название пула модулей по выбору"), max_length=256, blank=False, default=_("Название пула"))
    description = models.TextField(_("Описание"), max_length=16384, blank=True, default="")
    modules = models.ManyToManyField(Module)

    class Meta:
        verbose_name = 'пул модулей по выбору'
        verbose_name_plural = 'пулы модулей по выбору'

    def get_all(self):
        return "\n".join([str(module)for module in self.modules.all()])