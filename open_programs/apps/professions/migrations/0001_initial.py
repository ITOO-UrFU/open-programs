# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-07 15:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archived', models.BooleanField(default=False, verbose_name='В архиве')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('status', models.CharField(choices=[('h', 'Скрыт'), ('p', 'Опубликован')], default='h', max_length=1, verbose_name='Статус публикации')),
                ('title', models.CharField(default='', max_length=256, verbose_name='Название профессии')),
                ('description', models.TextField(blank=True, default='Здесь должно быть описание профессии', max_length=16384, verbose_name='Описание профессии')),
            ],
            options={
                'verbose_name': 'профессия',
                'verbose_name_plural': 'профессии',
            },
        ),
    ]