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


class GeneralBaseModulesPool(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("Название базового модуля программы"), max_length=256, blank=False, default=_("Название пула"))
    description = models.TextField(_("Описание"), max_length=16384, blank=True, default="")
    modules = models.ManyToManyField(Module)

    class Meta:
        verbose_name = 'базовый модуль программы'
        verbose_name_plural = 'базовые модули программы'

    def get_all(self):
        return "\n".join([str(module)for module in self.modules.all()])


class EducationalProgramTrajectoriesPool(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("Название пула модулей траектории обр. программ"), max_length=256, blank=False, default=_("Название пула"))
    description = models.TextField(_("Описание"), max_length=16384, blank=True, default="")
    modules = models.ManyToManyField(Module)

    class Meta:
        verbose_name = 'пул модулей траектории обр. программ'
        verbose_name_plural = 'пулы модулей траектории обр. программ'

    def get_all(self):
        return "\n".join([str(module)for module in self.modules.all()])


class ChoiceModulesPool(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("Название пула модулей по выбору"), max_length=256, blank=False, default=_("Название пула"))
    description = models.TextField(_("Описание"), max_length=16384, blank=True, default="")
    modules = models.ManyToManyField(Module)

    class Meta:
        verbose_name = 'пул модулей по выбору'
        verbose_name_plural = 'пулы модулей по выбору'

    def get_all(self):
        return "\n".join([str(module)for module in self.modules.all()])