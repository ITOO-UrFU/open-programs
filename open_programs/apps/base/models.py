from django.db import models
from django.utils.translation import ugettext_lazy as _

class ObjectBaseClass(models.Model):
    class Meta:
        abstract = True

    STATUSES = (
        ('h', _("Скрыт")),
        ('p', _("Опубликован")),
    )
    archived = models.BooleanField(_("В архиве"), default=False)
    created = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated = models.DateTimeField(_('Обновлен'), auto_now=True)
    status = models.CharField(_("Статус публикации"), max_length=1, choices=STATUSES, default='h')