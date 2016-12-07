# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-07 13:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archived', models.BooleanField(default=False, verbose_name='В архиве')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('status', models.CharField(choices=[('h', 'Скрыт'), ('p', 'Опубликован')], default='h', max_length=1, verbose_name='Статус публикации')),
                ('name', models.CharField(default='', max_length=256, verbose_name='Название дисциплины')),
                ('courses', models.ManyToManyField(to='courses.Course', verbose_name='Варианты реализации дисциплины')),
            ],
            options={
                'verbose_name': 'дисциплина',
                'verbose_name_plural': 'дисциплины',
            },
        ),
    ]
