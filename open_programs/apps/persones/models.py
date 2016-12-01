from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField

class Person(models.Model):
    first_name = models.CharField(_('Имя пользователя'), max_length=32, blank=False, default=_('Имя'))
    last_name = models.CharField(_('Фамилия пользователя'), max_length=32, blank=False, default=_('Фамилия'))
    second_name = models.CharField(_('Отчество пользователя'), max_length=32, blank=True, default=_('Отчество'))
    SEXES = (
        ('U', 'Не выбран',),
        ('F', 'Женский',),
        ('M', 'Мужской',),
     )
    sex = models.CharField(max_length=1,
                           choices=SEXES,
                           default='U'
                           )
    alt_email = models.EmailField(_('Альтернативный e-mail'),max_length=254, blank=True)
    country = CountryField()
    birthday_date = models.DateField(_('Дата рождения'), blank=True)
#   roles = models.ManyToManyField(ROLE)  TODO: Сделать модель 'Роль'
    biography = models.TextField(_('Биография пользователя'), blank=True, default=_('Биография'))


class AcademicDegree(models.Model):
    name = models.CharField(max_length=64)