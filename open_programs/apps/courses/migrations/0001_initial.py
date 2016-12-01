# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-01 15:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Название курса', max_length=256, verbose_name='Название курса')),
                ('description', models.TextField(blank=True, default='Здесь должно быть описание курса', max_length=16384, verbose_name='Описание')),
                ('slug', models.SlugField(help_text='должен быть уникальным в рамках вуза', verbose_name='Код курса')),
                ('archived', models.BooleanField(default=False, verbose_name='В архиве')),
                ('authors_ordering', models.CharField(blank=True, help_text='id авторов через пробел', max_length=500, verbose_name='Порядок авторов')),
                ('status', models.CharField(choices=[('h', 'Скрыт'), ('p', 'Опубликован')], default='h', max_length=1, verbose_name='Статус публикации')),
                ('about', models.TextField(blank=True, verbose_name='О курсе')),
                ('cover', models.ImageField(blank=True, upload_to='cover', verbose_name='Обложка')),
                ('video', models.URLField(blank=True, default='', help_text='URL видео', max_length=500, verbose_name='Промовидео')),
                ('video_cover', models.ImageField(blank=True, upload_to='video_cover', verbose_name='Картинка для видео')),
                ('workload', models.PositiveIntegerField(blank=True, null=True, verbose_name='часов в неделю')),
                ('points', models.PositiveIntegerField(blank=True, null=True, verbose_name='зачётных единиц')),
                ('duration', models.PositiveIntegerField(blank=True, null=True, verbose_name='Длительность (недель)')),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startdate', models.DateTimeField(verbose_name='Начало курса')),
                ('enddate', models.DateTimeField(verbose_name='Конец курса')),
            ],
        ),
    ]
