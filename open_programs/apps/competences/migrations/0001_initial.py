# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-17 19:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('results', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archived', models.BooleanField(default=False, verbose_name='В архиве')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('status', models.CharField(choices=[('h', 'Скрыт'), ('p', 'Опубликован')], default='h', max_length=1, verbose_name='Статус публикации')),
                ('title', models.CharField(default='', max_length=512, verbose_name='Компетенция')),
                ('results', models.ManyToManyField(to='results.Result', verbose_name='Результаты обучения')),
            ],
            options={
                'verbose_name': 'компетенция',
                'verbose_name_plural': 'компетенции',
            },
        ),
    ]
