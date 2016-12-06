# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-06 08:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('discipline', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChoiceModulesPool',
            fields=[
                ('archived', models.BooleanField(default=False, verbose_name='В архиве')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('status', models.CharField(choices=[('h', 'Скрыт'), ('p', 'Опубликован')], default='h', max_length=1, verbose_name='Статус публикации')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(default='Название пула', max_length=256, verbose_name='Название пула модулей по выбору')),
                ('description', models.TextField(blank=True, default='', max_length=16384, verbose_name='Описание')),
            ],
            options={
                'verbose_name_plural': 'пулы модулей по выбору',
                'verbose_name': 'пул модулей по выбору',
            },
        ),
        migrations.CreateModel(
            name='EducationalProgramTrajectoriesPool',
            fields=[
                ('archived', models.BooleanField(default=False, verbose_name='В архиве')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('status', models.CharField(choices=[('h', 'Скрыт'), ('p', 'Опубликован')], default='h', max_length=1, verbose_name='Статус публикации')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(default='Название пула', max_length=256, verbose_name='Название пула модулей траектории обр. программ')),
                ('description', models.TextField(blank=True, default='', max_length=16384, verbose_name='Описание')),
            ],
            options={
                'verbose_name_plural': 'пулы модулей траектории обр. программ',
                'verbose_name': 'пул модулей траектории обр. программ',
            },
        ),
        migrations.CreateModel(
            name='GeneralBaseModulesPool',
            fields=[
                ('archived', models.BooleanField(default=False, verbose_name='В архиве')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('status', models.CharField(choices=[('h', 'Скрыт'), ('p', 'Опубликован')], default='h', max_length=1, verbose_name='Статус публикации')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(default='Название пула', max_length=256, verbose_name='Название базового модуля программы')),
                ('description', models.TextField(blank=True, default='', max_length=16384, verbose_name='Описание')),
            ],
            options={
                'verbose_name_plural': 'базовые модули программы',
                'verbose_name': 'базовый модуль программы',
            },
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('archived', models.BooleanField(default=False, verbose_name='В архиве')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('status', models.CharField(choices=[('h', 'Скрыт'), ('p', 'Опубликован')], default='h', max_length=1, verbose_name='Статус публикации')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(default='Название модуля', max_length=256, verbose_name='Название модуля')),
                ('description', models.TextField(blank=True, default='', max_length=16384, verbose_name='Описание модуля')),
                ('disciplines', models.ManyToManyField(to='discipline.Discipline', verbose_name='Дисциплины')),
            ],
            options={
                'verbose_name_plural': 'модули',
                'verbose_name': 'модуль',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archived', models.BooleanField(default=False, verbose_name='В архиве')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('status', models.CharField(choices=[('h', 'Скрыт'), ('p', 'Опубликован')], default='h', max_length=1, verbose_name='Статус публикации')),
                ('title', models.CharField(default='Название типа модуля', max_length=256, verbose_name='Название типа модуля')),
                ('description', models.TextField(blank=True, default='', max_length=16384, verbose_name='Описание')),
            ],
            options={
                'verbose_name_plural': 'типы модулей',
                'verbose_name': 'тип модуля',
            },
        ),
        migrations.AddField(
            model_name='module',
            name='type',
            field=models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to='modules.Type', verbose_name='Тип модуля'),
        ),
        migrations.AddField(
            model_name='generalbasemodulespool',
            name='modules',
            field=models.ManyToManyField(to='modules.Module'),
        ),
        migrations.AddField(
            model_name='educationalprogramtrajectoriespool',
            name='modules',
            field=models.ManyToManyField(to='modules.Module'),
        ),
        migrations.AddField(
            model_name='choicemodulespool',
            name='modules',
            field=models.ManyToManyField(to='modules.Module'),
        ),
    ]
