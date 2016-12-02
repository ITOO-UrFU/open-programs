from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(_('Имя пользователя'), max_length=32, blank=False, default='')
    last_name = models.CharField(_('Фамилия пользователя'), max_length=32, blank=False, default='')
    second_name = models.CharField(_('Отчество пользователя'), max_length=32, blank=True, default='')
    SEXES = (
        ('U', _('Не выбран')),
        ('F', _('Женский')),
        ('M', _('Мужской')),
     )
    sex = models.CharField(max_length=1,
                           choices=SEXES,
                           default='U'
                           )
    alt_email = models.EmailField(_('Альтернативный e-mail'),max_length=254, blank=True)
    country = CountryField(blank=True, default='Russia')
    birthday_date = models.DateField(_('Дата рождения'), null=True, blank=True)
#   roles = models.ManyToManyField(ROLE)  TODO: Сделать модель 'Роль'
    biography = models.TextField(_('Биография пользователя'), blank=True, default='')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Person.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.person.save()


class AcademicDegree(models.Model):
    name = models.CharField(max_length=64)