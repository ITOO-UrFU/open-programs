# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-03 13:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicDegree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=32, verbose_name='Имя пользователя')),
                ('last_name', models.CharField(default='', max_length=32, verbose_name='Фамилия пользователя')),
                ('second_name', models.CharField(blank=True, default='', max_length=32, verbose_name='Отчество пользователя')),
                ('sex', models.CharField(choices=[('U', 'Не выбран'), ('F', 'Женский'), ('M', 'Мужской')], default='U', max_length=1)),
                ('alt_email', models.EmailField(blank=True, max_length=254, verbose_name='Альтернативный e-mail')),
                ('country', django_countries.fields.CountryField(blank=True, default='Russia', max_length=2)),
                ('birthday_date', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('biography', models.TextField(blank=True, default='', verbose_name='Биография пользователя')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'персона',
                'verbose_name_plural': 'персоны',
            },
        ),
    ]
