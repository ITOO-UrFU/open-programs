# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-17 19:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=32)),
                ('okso', models.CharField(max_length=8)),
                ('title', models.CharField(max_length=1024)),
                ('ministerialCode', models.CharField(max_length=8)),
                ('ugnTitle', models.CharField(max_length=64)),
                ('standard', models.CharField(max_length=32)),
                ('qualifications', models.ManyToManyField(to='uni.Qualification')),
            ],
        ),
    ]
