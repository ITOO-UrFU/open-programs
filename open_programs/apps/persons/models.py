from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Person(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(_('Имя пользователя'), max_length=32, blank=True, null=True, default='')
    last_name = models.CharField(_('Фамилия пользователя'), max_length=32, blank=True, null=True, default='')
    second_name = models.CharField(_('Отчество пользователя'), max_length=32, blank=True, null=True, default='')
    SEXES = (
        ('U', _('Не выбран')),
        ('F', _('Женский')),
        ('M', _('Мужской')),
    )
    sex = models.CharField(max_length=1,
                           choices=SEXES,
                           default='U'
                           )
    alt_email = models.EmailField(_('Альтернативный e-mail'), max_length=254, blank=True, null=True,)
    country = CountryField(blank=True, default='RU')
    birthday_date = models.DateField(_('Дата рождения'), null=True, blank=True)
#   roles = models.ManyToManyField(ROLE)  TODO: Сделать модель 'Роль'
    biography = models.TextField(_('Биография пользователя'), blank=True, null=True)

    class Meta:
        verbose_name = 'персона'
        verbose_name_plural = 'персоны'
        app_label = "persons"

    def __str__(self):
        if self.first_name and self.last_name:
            return ' '.join([str(self.last_name), str(self.first_name), str(self.second_name)])
        else:
            return str(self.user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Person.objects.create(user=instance)



class AcademicDegree(models.Model):
    name = models.CharField(max_length=64)
