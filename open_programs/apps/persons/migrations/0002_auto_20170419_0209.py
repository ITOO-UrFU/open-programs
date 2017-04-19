# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-18 21:09
from __future__ import unicode_literals

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='country',
            field=django_countries.fields.CountryField(blank=True, default='RU', max_length=2),
        ),
    ]