# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-02 20:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persones', '0004_person_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name': 'персона', 'verbose_name_plural': 'персоны'},
        ),
    ]
