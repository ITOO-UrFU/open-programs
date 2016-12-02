# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-02 16:16
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChoicePool',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(default='Название пула', max_length=256, verbose_name='Название пула модулей по выбору')),
                ('description', models.TextField(blank=True, default='', max_length=16384, verbose_name='Описание')),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(default='Название модуля', max_length=256, verbose_name='Название модуля')),
                ('description', models.TextField(blank=True, default='', max_length=16384, verbose_name='Описание модуля')),
            ],
        ),
        migrations.CreateModel(
            name='ModulesPool',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(default='Название пула', max_length=256, verbose_name='Название пула модулей для траектории образовательной программы')),
                ('description', models.TextField(blank=True, default='', max_length=16384, verbose_name='Описание')),
                ('modules', models.ManyToManyField(to='modules.Module')),
            ],
        ),
        migrations.AddField(
            model_name='choicepool',
            name='modules',
            field=models.ManyToManyField(to='modules.Module'),
        ),
    ]