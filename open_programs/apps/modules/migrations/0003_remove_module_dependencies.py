# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-12 20:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0002_auto_20161213_0028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='dependencies',
        ),
    ]
