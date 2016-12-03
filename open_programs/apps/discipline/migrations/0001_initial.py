# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-03 13:12
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
                ('name', models.CharField(default='', max_length=256, verbose_name='Название дисциплины')),
                ('courses', models.ManyToManyField(to='courses.Course', verbose_name='Варианты реализации дисциплины')),
            ],
            options={
                'verbose_name': 'дисциплина',
                'verbose_name_plural': 'дисциплины',
            },
        ),
    ]
