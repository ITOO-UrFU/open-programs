# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-09 11:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disciplines', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discipline',
            name='courses',
            field=models.ManyToManyField(blank=True, to='courses.Course', verbose_name='Варианты реализации дисциплины'),
        ),
        migrations.AlterField(
            model_name='discipline',
            name='results',
            field=models.ManyToManyField(blank=True, to='results.Result', verbose_name='Результаты обучения'),
        ),
    ]